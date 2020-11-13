"""Sample sensor built from Datadog sensor (For now, to be changed)"""

from typing import Any, Callable, Dict, List, Optional

from datadog import api

from airflow.exceptions import AirflowException
from airflow.providers.datadog.hooks.datadog import DatadogHook
from airflow.sensors.base_sensor_operator import BaseSensorOperator
from airflow.utils.decorators import apply_defaults


class SampleSensor(BaseSensorOperator):
    """
    This is where I will provide documentation for my sensor. As of now, this is a replication of the DataDog sensor.
    Below is where I will document the available params for this sensor.

    :param datadog_conn_id: The connection to datadog, containing metadata for api keys.
    :param datadog_conn_id: str
    """

    ui_color = '#66c3dd'

    @apply_defaults
    def __init__(
        self,
        *,
        datadog_conn_id: str = 'datadog_default',
        from_seconds_ago: int = 3600,
        up_to_seconds_from_now: int = 0,
        priority: Optional[str] = None,
        sources: Optional[str] = None,
        tags: Optional[List[str]] = None,
        response_check: Optional[Callable[[Dict[str, Any]], bool]] = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.datadog_conn_id = datadog_conn_id
        self.from_seconds_ago = from_seconds_ago
        self.up_to_seconds_from_now = up_to_seconds_from_now
        self.priority = priority
        self.sources = sources
        self.tags = tags
        self.response_check = response_check

    def poke(self, context: Dict[str, Any]) -> bool:
        # This instantiates the hook, but doesn't need it further,
        # because the API authenticates globally (unfortunately),
        # but for airflow this shouldn't matter too much, because each
        # task instance runs in its own process anyway.
        DatadogHook(datadog_conn_id=self.datadog_conn_id)

        response = api.Event.query(
            start=self.from_seconds_ago,
            end=self.up_to_seconds_from_now,
            priority=self.priority,
            sources=self.sources,
            tags=self.tags,
        )

        if isinstance(response, dict) and response.get('status', 'ok') != 'ok':
            self.log.error("Unexpected Datadog result: %s", response)
            raise AirflowException("Datadog returned unexpected result")

        if self.response_check:
            # run content check on response
            return self.response_check(response)

        # If no check was inserted, assume any event that matched yields true.
        return len(response) > 0