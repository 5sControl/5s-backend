import pyodbc

from typing import List, Optional, Any

from src.DatabaseConnections.models import DatabaseConnection

from .base import BaseReadOnlyRepository


class MsSqlServerRepository(BaseReadOnlyRepository):
    def __init__(self):
        self.driver = "{ODBC Driver 17 for SQL Server}"
        self.connector = pyodbc

    def execute_query(
        self, query: str, parameters: Optional[List[Any]] = None
    ) -> List[Any]:
        with self.connector.connect(self.connection_string) as connection:
            cursor = connection.cursor()

            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)

            result = cursor.fetchall()
            cursor.close()

            return result

    def is_stable(self, server: str, database: str, username: str, password: str, port: int) -> bool:
        conn_str = self._get_connection_string(server, database, username, password, port)
        try:
            conn = self.connector.connect(conn_str)
            conn.close()
        except Exception:
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
            return f"SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};DRIVER={self.driver};TrustServerCertificate=yes"
        else:
            db_obj: DatabaseConnection = self.__get_credentials()
            return f"SERVER={db_obj.server};PORT={db_obj.port};DATABASE={db_obj.database};UID={db_obj.username};PWD={db_obj.password};DRIVER={self.driver};TrustServerCertificate=yes"

    def __get_credentials(self):
        return DatabaseConnection.objects.get(dbms="mssql")
