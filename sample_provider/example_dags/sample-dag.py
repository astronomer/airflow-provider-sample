from pendulum import datetime

from airflow.decorators import dag

from sample_provider.operators.sample import SampleOperator
from sample_provider.sensors.sample import SampleSensor


@dag(
    start_date=datetime(2022, 1, 1),
    schedule=None,
    # ``default_args`` will get passed on to each task. You can override them on a per-task basis during
    # operator initialization.
    default_args={"retries": 2, "sample_conn_id": "conn_sample"},
    tags=["example"],
    default_view="graph",
)
def sample_workflow():
    """
    ### Sample DAG

    Showcases the sample provider package's operator and sensor.

    To run this example, create an HTTP connection with:
    - id: conn_sample
    - type: http
    - host: www.httpbin.org
    """

    task_get_op = SampleOperator(task_id="get_op", method="get")

    task_sensor = SampleSensor(task_id="sensor", endpoint="")

    task_get_op >> task_sensor


sample_workflow()
