from __future__ import annotations

from typing import Any

import requests
from requests.auth import HTTPBasicAuth

from airflow.hooks.base import BaseHook


class SampleHook(BaseHook):
    """
    Sample Hook that interacts with an HTTP endpoint the Python requests library.

    :param method: the API method to be called
    :type method: str
    :param sample_conn_id: connection that has the base API url i.e https://www.google.com/
        and optional authentication credentials. Default headers can also be specified in
        the Extra field in json format.
    :type sample_conn_id: str
    :param auth_type: The auth type for the service
    :type auth_type: AuthBase of python requests lib
    """

    conn_name_attr = "sample_conn_id"
    default_conn_name = "sample_default"
    conn_type = "sample"
    hook_name = "Sample"

    @staticmethod
    def get_connection_form_widgets() -> dict[str, Any]:
        """Returns connection widgets to add to connection form"""
        from flask_appbuilder.fieldwidgets import BS3PasswordFieldWidget, BS3TextFieldWidget
        from flask_babel import lazy_gettext
        from wtforms import PasswordField, StringField

        return {
            "account": StringField(lazy_gettext("Account"), widget=BS3TextFieldWidget()),
            "secret_key": PasswordField(lazy_gettext("Secret Key"), widget=BS3PasswordFieldWidget()),
        }

    @staticmethod
    def get_ui_field_behaviour() -> dict:
        """Returns custom field behaviour"""
        import json

        return {
            "hidden_fields": ["port", "password", "login", "schema"],
            "relabeling": {},
            "placeholders": {
                "extra": json.dumps(
                    {
                        "example_parameter": "parameter",
                    },
                    indent=4,
                ),
                "account": "HeirFlough",
                "secret_key": "mY53cr3tk3y!",
                "host": "https://www.httpbin.org",
            },
        }

    def __init__(
        self,
        method: str = "POST",
        sample_conn_id: str = default_conn_name,
        auth_type: Any = HTTPBasicAuth,
    ) -> None:
        super().__init__()
        self.sample_conn_id = sample_conn_id
        self.method = method.upper()
        self.base_url: str = ""
        self.auth_type: Any = auth_type

    def get_conn(self, headers: dict[str, Any] | None = None) -> requests.Session:
        """
        Returns http session to use with requests.

        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """
        session = requests.Session()

        if self.sample_conn_id:
            conn = self.get_connection(self.sample_conn_id)

            if conn.host and "://" in conn.host:
                self.base_url = conn.host
            else:
                # schema defaults to HTTP
                schema = conn.schema if conn.schema else "http"
                host = conn.host if conn.host else ""
                self.base_url = schema + "://" + host

            if conn.port:
                self.base_url = self.base_url + ":" + str(conn.port)
            if conn.login:
                session.auth = self.auth_type(conn.login, conn.password)
            if conn.extra:
                try:
                    session.headers.update(conn.extra_dejson)
                except TypeError:
                    self.log.warning("Connection to %s has invalid extra field.", conn.host)
        if headers:
            session.headers.update(headers)

        return session

    def run(
        self,
        endpoint: str | None = None,
        data: dict[str, Any] | str | None = None,
        headers: dict[str, Any] | None = None,
        **request_kwargs,
    ) -> Any:
        """
        Performs the request

        :param endpoint: the endpoint to be called i.e. resource/v1/query?
        :type endpoint: str
        :param data: payload to be uploaded or request parameters
        :type data: dict
        :param headers: additional headers to be passed through as a dictionary
        :type headers: dict
        """

        session = self.get_conn(headers)

        if self.base_url and not self.base_url.endswith("/") and endpoint and not endpoint.startswith("/"):
            url = self.base_url + "/" + endpoint
        else:
            url = (self.base_url or "") + (endpoint or "")

        if self.method == "GET":
            # GET uses params
            req = requests.Request(self.method, url, headers=headers)
        else:
            # Others use data
            req = requests.Request(self.method, url, data=data, headers=headers)

        prepped_request = session.prepare_request(req)

        self.log.info("Sending %r to url: %s", self.method, url)

        try:
            response = session.send(prepped_request)
            return response

        except requests.exceptions.ConnectionError as ex:
            self.log.warning("%s Tenacity will retry to execute the operation", ex)
            raise ex
