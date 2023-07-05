from typing import Any, Dict
import pyodbc
import pymssql


class PyodbcConnector:
    def __init__(self):
        self.connection = None
        self.driver = "{ODBC Driver 17 for SQL Server}"

    def connect(self, connection_data: Dict[str, Any]):
        host = connection_data["host"]
        database = connection_data["database"]
        port = connection_data["port"]
        user = connection_data["user"]
        password = connection_data["password"]
        self.connection = pyodbc.connect(f"SERVER={host};PORT={port};DATABASE={database};UID={user};PWD={password};DRIVER={self.driver};TrustServerCertificate=yes")

    def close(self):
        if self.connection:
            self.connection.close()

    def cursor(self):
        return self.connection.cursor()


class PymssqlConnector:
    def __init__(self):
        self.connection = None

    def connect(self, connection_string: str):
        self.connection = pymssql.connect(**connection_string)

    def close(self):
        if self.connection:
            self.connection.close()

    def cursor(self):
        return self.connection.cursor(as_dict=False)
