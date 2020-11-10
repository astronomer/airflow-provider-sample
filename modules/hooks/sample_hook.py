"""Sample hook built from BaseHook"""
import logging
import random
from typing import Any, List

from airflow.models.connection import Connection
from airflow.utils.log.logging_mixin import LoggingMixin

log = logging.getLogger(__name__)


class SampleHook(LoggingMixin):
    """
    Here is where I will document my hook.

    This file is an abstract base class for hooks, which are meant as an interface to
    interact with external systems.
    """

    @classmethod
    def get_connections(cls, conn_id: str) -> List[Connection]:
        """
        Get all connections as an iterable.

        :param conn_id: connection id
        :return: array of connections
        """
        return Connection.get_connections_from_secrets(conn_id)

    @classmethod
    def get_connection(cls, conn_id: str) -> Connection:
        """
        Get random connection selected from all connections configured with this connection id.

        :param conn_id: connection id
        :return: connection
        """
        conn = random.choice(cls.get_connections(conn_id))
        if conn.host:
            log.info(
                "Using connection to: id: %s. Host: %s, Port: %s, Schema: %s, Login: %s, Password: %s, "
                "extra: %s",
                conn.conn_id,
                conn.host,
                conn.port,
                conn.schema,
                conn.login,
                "XXXXXXXX" if conn.password else None,
                "XXXXXXXX" if conn.extra_dejson else None,
            )
        return conn

    @classmethod
    def get_hook(cls, conn_id: str) -> "BaseHook":
        """
        Returns default hook for this connection id.

        :param conn_id: connection id
        :return: default hook for this connection
        """
        # TODO: set method return type to BaseHook class when on 3.7+.
        #  See https://stackoverflow.com/a/33533514/3066428
        connection = cls.get_connection(conn_id)
        return connection.get_hook()

    def get_conn(self) -> Any:
        """Returns connection for the hook."""
        raise NotImplementedError()