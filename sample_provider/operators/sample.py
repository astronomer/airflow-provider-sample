from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator, BaseOperatorLink

from sample_provider.hooks.sample import SampleHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class SampleOperatorExtraLink(BaseOperatorLink):

    name = "Astronomer Registry"

    def get_link(self, operator: BaseOperator, *, ti_key=None):
        return "https://registry.astronomer.io"


class SampleOperator(BaseOperator):
    """
    Calls an endpoint on an HTTP system to execute an action.

    :param sample_conn_id: connection to run the operator with
    :type sample_conn_id: str
    :param endpoint: The relative part of the full url. (templated)
    :type endpoint: str
    :param method: The HTTP method to use, default = "POST"
    :type method: str
    :param data: The data to pass
    :type data: a dictionary of key/value string pairs
    :param headers: The HTTP headers to be added to the request
    :type headers: a dictionary of string key/value pairs
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = [
        "endpoint",
        "data",
        "headers",
    ]
    template_fields_renderers = {"headers": "json", "data": "py"}
    template_ext = ()
    ui_color = "#f4a460"

    operator_extra_links = (SampleOperatorExtraLink(),)

    def __init__(
        self,
        *,
        endpoint: str | None = None,
        method: str = "POST",
        data: Any | None = None,
        headers: dict[str, str] | None = None,
        extra_options: dict[str, Any] | None = None,
        sample_conn_id: str = SampleHook.default_conn_name,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.sample_conn_id = sample_conn_id
        self.method = method
        self.endpoint = endpoint
        self.headers = headers or {}
        self.data = data or {}
        self.extra_options = extra_options or {}
        if kwargs.get("xcom_push") is not None:
            raise AirflowException("'xcom_push' was deprecated, use 'BaseOperator.do_xcom_push' instead")

    def execute(self, context: Context) -> Any:
        hook = SampleHook(self.method, sample_conn_id=self.sample_conn_id)

        self.log.info("Call HTTP method")
        response = hook.run(self.endpoint, self.data, self.headers)

        return response.text
