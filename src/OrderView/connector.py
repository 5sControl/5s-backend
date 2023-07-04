from typing import Any, Iterable, Optional
import pyodbc

from rest_framework.response import Response
from rest_framework import status
from src.Core.types import Query
from src.DatabaseConnections.models import DatabaseConnection


class MsSqlConnector:
    def __init__(self):
        self.driver = "{ODBC Driver 17 for SQL Server}"

    def is_stable(self, credentials):
        server = credentials["server"]
        database = credentials["database"]
        username = credentials["username"]
        password = credentials["password"]
        port = credentials["port"]

        if not (
            self._is_database_connection_exist(
                server=server, database=database, username=username, port=port
            )
            & self._is_database_connection_is_stable(
                server=server,
                database=database,
                username=username,
                password=password,
                port=port,
            )
        ):
            return False
        return True

    def _is_database_connection_exist(self, server, database, username, port):
        if DatabaseConnection.objects.filter(
            server=server, database=database, username=username
        ):
            return False
        return True

    def _is_database_connection_is_stable(
        self, server, database, username, password, port
    ):
        conn_str = self._get_connection_string(
            server, database, username, password, self.driver, port
        )

        try:
            conn = pyodbc.connect(conn_str)
            conn.close()
            return True
        except pyodbc.Error:
            return False

    def get_database_connection(self):
        connection_data = (
            DatabaseConnection.objects.all()
            .values()
            .first()  # FIXME: should be by database type
        )

        server = connection_data["server"]
        database = connection_data["database"]
        username = connection_data["username"]
        password = connection_data["password"]
        port = connection_data["port"]

        conn_str = self._get_connection_string(
            server, database, username, password, self.driver, port
        )

        connection = pyodbc.connect(conn_str)

        return connection

    def _get_connection_string(
        self, server, database, username, password, driver, port
    ):
        return f"SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password};DRIVER={driver};TrustServerCertificate=yes"  # noqa

    def get_conections(self):
        return DatabaseConnection.objects.all()

    def delete_connection(self, id):
        DatabaseConnection.objects.get(id=id).delete()
        return True

    def check_database_connection(self, func):
        def wrapper(*args, **kwargs):
            if DatabaseConnection.objects.first() is not None:
                return func(*args, **kwargs)
            else:
                response_data = {
                    "status": False,
                    "message": "database connection doesnt exist",
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

        return wrapper

    def executer(
        self,
        connection: pyodbc.Connection,
        query: Query,
        params: Optional[Iterable[Any]] = None,
    ) -> Any:
        with connection.cursor() as cursor:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            results = cursor.fetchall()

        return results


connector = MsSqlConnector()
