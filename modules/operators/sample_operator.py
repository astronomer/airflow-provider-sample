"""Sample HelloWorld Operator"""
import logging

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.utils.decorators import apply_defaults

log = logging.getLogger(__name__)

class SampleOperator(BaseOperator):
    """
    Insert your operator documentation here. This operator inherits from the BaseOperator and prints "Hello World!" and whatever string that I choose to pass as an argument.

    Here is where we'll include our params
    :param str my_operator_param: A random string to pass to the operator that will be printed after "Hello World!"
    """

    @apply_defaults
    def __init__(self, my_operator_param, *args, **kwargs):
        self.operator_param = my_operator_param
        super(MyFirstOperator, self).__init__(*args, **kwargs)

    def execute(self, context):
        log.info("Hello World!")
        log.info('operator_param: %s', self.operator_param)