"""Sample HelloWorld Operator"""
import logging

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)


class SampleOperator(BaseOperator):
    """
    [Short description here explaining what the operator does] This operator prints both "Hello World!" and whatever string that I choose to pass as a parameter.

    [Long description explaining how it works and including any necessary code blocks or notes] This operator extends the BaseOperator.

    [Params with descriptions]
    :param provider_conn_id: The connection to provider, containing metadata for api keys.
    :param provider_conn_id: str    
    """

    @apply_defaults
    def __init__(self, my_operator_param, *args, **kwargs):
        self.operator_param = my_operator_param
        super(MyFirstOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        log.info("Hello World!")
        log.info('operator_param: %s', self.operator_param)
