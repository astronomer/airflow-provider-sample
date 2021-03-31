from typing import Any, Callable, Dict, Optional

from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

from sample_provider.hooks.sample_hook import SampleHook


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
        'endpoint',
        'data',
        'headers',
    ]
    template_fields_renderers = {'headers': 'json', 'data': 'py'}
    template_ext = ()
    ui_color = '#f4a460'

    @apply_defaults
    def __init__(
        self,
        *,
        endpoint: Optional[str] = None,
        method: str = 'POST',
        data: Any = None,
        headers: Optional[Dict[str, str]] = None,
        extra_options: Optional[Dict[str, Any]] = None,
        sample_conn_id: str = 'conn_sample',
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.sample_conn_id = sample_conn_id
        self.method = method
        self.endpoint = endpoint
        self.headers = headers or {}
        self.data = data or {}
        self.extra_options = extra_options or {}
        if kwargs.get('xcom_push') is not None:
            raise AirflowException(
                "'xcom_push' was deprecated, use 'BaseOperator.do_xcom_push' instead")

    def execute(self, context: Dict[str, Any]) -> Any:

        hook = SampleHook(self.method, sample_conn_id=self.sample_conn_id)

        self.log.info("Call HTTP method")

        response = hook.run(self.endpoint, self.data, self.headers)

        return response.text
