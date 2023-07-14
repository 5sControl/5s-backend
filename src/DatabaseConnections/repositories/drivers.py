from typing import Any, Dict
import pymssql


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
