"""
Unittest module to test Operators.

Requires the unittest, pytest, and requests-mock Python libraries.

Run test:

    python3 -m unittest tests.operators.test_sample_operator.TestSampleOperator

"""

import json
import logging
import os
import pytest
import requests_mock
from unittest import mock

# Import Operator
from sample_provider.operators.sample import SampleOperator


log = logging.getLogger(__name__)


# Mock the `conn_sample` Airflow connection
@mock.patch.dict('os.environ', AIRFLOW_CONN_CONN_SAMPLE='http://https%3A%2F%2Fwww.httpbin.org%2F')
class TestSampleOperator:
    """
    Test Sample Operator.
    """

    @requests_mock.mock()
    def test_operator(self, m):

        # Mock endpoint
        m.get('https://www.httpbin.org/', json={'data': 'mocked response'})

        operator = SampleOperator(
            task_id='run_operator',
            sample_conn_id='conn_sample',
            method='get'
        )

        # Airflow calls the operator's execute method at runtime with the task run's bespoke context dictionary
        response_payload = operator.execute(context={})
        response_payload_json = json.loads(response_payload)

        log.info(response_payload_json)

        # Assert the API call returns expected mocked payload
        assert response_payload_json['data'] == 'mocked response'

