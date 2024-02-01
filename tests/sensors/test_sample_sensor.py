"""
Unittest module to test Operators.

Requires the unittest, pytest, and requests-mock Python libraries.

Run test:

    python3 -m unittest tests.sensors.test_sample_sensor.TestSampleSensor

"""

import logging
from unittest import mock

# Import Sensor
from sample_provider.sensors.sample import SampleSensor


log = logging.getLogger(__name__)


# Mock the `conn_sample` Airflow connection
@mock.patch.dict('os.environ', AIRFLOW_CONN_CONN_SAMPLE='http://https%3A%2F%2Fwww.httpbin.org%2F')
class TestSampleSensor:
    """
    Test Sample Sensor.
    """

    def test_sensor_success(self, requests_mock):

        # Mock endpoint
        requests_mock.get('https://www.httpbin.org/check_status')

        operator = SampleSensor(
            task_id='sample_sensor_check',
            sample_conn_id='conn_sample',
            endpoint='check_status'
        )

        # Assert poke returns True
        assert operator.poke(context={}) == True

    def test_sensor_fail(self, requests_mock):

        # Mock endpoint
        requests_mock.get('https://www.httpbin.org/check_status', status_code=404)

        operator = SampleSensor(
            task_id='sample_sensor_check',
            sample_conn_id='conn_sample',
            endpoint='check_status'
        )

        # Assert poke returns False when endpoint returns 404
        assert operator.poke(context={}) == False


if __name__ == '__main__':
    unittest.main()
