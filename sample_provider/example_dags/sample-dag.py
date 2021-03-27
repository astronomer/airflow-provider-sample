from datetime import timedelta
import json

from airflow.decorators import dag, task
from airflow.utils.dates import days_ago

from sample_provider.operators.sample_operator import SampleOperator
from sample_provider.sensors.sample_sensor import SampleSensor


# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
}


@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2), tags=['example'])
def sample_worflow():
    """
    ### Sample DAG

    Showcases the sample provider package's operator and sensor.

    To run this example, create a connector with:
    - id: conn_sample
    - type: http
    - host: www.httpbin.org	
    """

    task_get_op = SampleOperator(
        task_id='get_op',
        sample_conn_id='conn_sample',
        method='get',
    )

    task_sensor = SampleSensor(
        task_id='sensor',
        sample_conn_id='conn_sample',
        endpoint=''
    )

    task_get_op >> task_sensor


sample_worflow_dag = sample_worflow()
