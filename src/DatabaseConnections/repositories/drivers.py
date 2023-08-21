from typing import Dict
import pymssql


class PymssqlConnector:
    def __init__(self):
        self.connection = None

    def connect(self, connection_data: Dict[str, str]):
        self.connection = pymssql.connect(
            server=connection_data["host"],
            port=connection_data["port"],
            user=connection_data["user"],
            password=connection_data["password"],
            database=connection_data["database"],
        )

    def close(self):
        if self.connection:
            self.connection.close()

    def cursor(self):
        return self.connection.cursor(as_dict=False)
