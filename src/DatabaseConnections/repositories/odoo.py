from typing import Any, List, Optional

import psycopg2

from src.Core.types import Query
from src.DatabaseConnections.models import DatabaseConnection
from src.DatabaseConnections.repositories.base import BaseReadOnlyRepository


class OdooRepository(BaseReadOnlyRepository):
    def __init__(self):
        self.connector = psycopg2

    def execute_query(
        self, query: Query, parameters: Optional[List[Any]] = None
    ) -> List[Any]:
        connection_string: str = self._get_connection_string()
        self.connector.connect(connection_string)
        cursor = self.connector.cursor()

        if parameters:
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
        connection_string: dict = self._get_connection_string(
            server, database, username, password, port
        )
        try:
            conn = self.connector.connect(**connection_string)
            conn.close()
            return True
        except Exception:
            return False

    def _get_connection_string(
        self,
        server: str = "",
        database: str = "",
        username: str = "",
        password: str = "",
        port: int = 0,
    ) -> dict:
        if server and database and username and password and port:
            return {
                "host": server,
                "user": username,
                "password": password,
                "database": database,
                "port": port,
            }
        else:
            db_obj: DatabaseConnection = DatabaseConnection.objects.get(is_active=True)
            return {
                "host": db_obj.server,
                "user": db_obj.username,
                "password": db_obj.password,
                "database": db_obj.database,
                "port": db_obj.port,
            }

psycopg2.connect