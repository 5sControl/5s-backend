import logging
from typing import List, Optional, Any

from src.Core.types import Query
from src.DatabaseConnections.models import ConnectionInfo

from .base import BaseReadOnlyRepository
from .drivers import PymssqlConnector

logger = logging.getLogger(__name__)


class WinHRepository(BaseReadOnlyRepository):
    def __init__(self):
        self.connector = PymssqlConnector()

    def execute_query(
        self, query: Query, parameters: Optional[List[Any]] = None
    ) -> List[Any]:
        connection_string: str = self._get_connection_string()
        self.connector.connect(connection_string)
        cursor = self.connector.cursor()

        if parameters:
            if isinstance(self.connector, PymssqlConnector):
                query = query.replace("?", "%s")
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)

        result = cursor.fetchall()
        cursor.close()
        self.connector.close()

        return result

    def is_stable(
        self, server: str, database: str, username: str, password: str, port: int
    ) -> bool:
        conn_str = self._get_connection_string(
            server, database, username, password, port
        )
        try:
            self.connector.connect(conn_str)
            self.connector.close()
        except Exception as e:
            logger.critical(f"Connection failed: {e}")
            return False
        return True

    def _get_connection_string(
        self,
        server: str = "",
        database: str = "",
        username: str = "",
        password: str = "",
        port: int = 0,
    ) -> str:
        if server and database and username and password and port:
            return {
                "host": server,
                "user": username,
                "password": password,
                "database": database,
                "port": port,
            }
        else:
            db_obj: ConnectionInfo = ConnectionInfo.objects.get(type="database")
            return {
                "host": db_obj.server,
                "user": db_obj.username,
                "password": db_obj.password,
                "database": db_obj.database,
                "port": db_obj.port,
            }
