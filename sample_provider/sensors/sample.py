from __future__ import annotations

from typing import TYPE_CHECKING, Any

from airflow.exceptions import AirflowException
from airflow.sensors.base import BaseSensorOperator

from sample_provider.hooks.sample import SampleHook

if TYPE_CHECKING:
    from airflow.utils.context import Context


class SampleSensor(BaseSensorOperator):
    """
    Executes a HTTP GET statement and returns False on failure caused by 404 Not Found.

    :param sample_conn_id: The connection to run the sensor against
    :type sample_conn_id: str
    :param method: The HTTP request method to use
    :type method: str
    :param endpoint: The relative part of the full url
    :type endpoint: str
    :param request_params: The parameters to be added to the GET url
    :type request_params: a dictionary of string key/value pairs
    :param headers: The HTTP headers to be added to the GET request
    :type headers: a dictionary of string key/value pairs
    """

    # Specify the arguments that are allowed to parse with jinja templating
    template_fields = [
        "endpoint",
        "request_params",
        "headers",
    ]

    def __init__(
        self,
        *,
        endpoint: str,
        sample_conn_id: str = SampleHook.default_conn_name,
        method: str = "GET",
        request_params: dict[str, Any] | None = None,
        headers: dict[str, Any] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.endpoint = endpoint
        self.sample_conn_id = sample_conn_id
        self.request_params = request_params or {}
        self.headers = headers or {}

        self.hook = SampleHook(method=method, sample_conn_id=sample_conn_id)

    def poke(self, context: Context) -> bool:
        self.log.info("Poking: %s", self.endpoint)
        try:
            response = self.hook.run(
                self.endpoint,
                data=self.request_params,
                headers=self.headers,
            )
            if response.status_code == 404:
                return False

        except AirflowException as exc:
            if str(exc).startswith("404"):
                return False

            raise exc

        return True
