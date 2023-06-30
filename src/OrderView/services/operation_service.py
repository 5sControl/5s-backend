from typing import List, Iterable

import pyodbc

from src.DatabaseConnections.services import connector as connector_service


class OperationService:
    def __init__(
        self,
    ):
        self.query = """
            SELECT DISTINCT Raport
            FROM Stanowiska
        """

    def get_operation_names(self) -> List[str]:
        connection: pyodbc.Connection = connector_service.get_database_connection()
        list_of_names: List[str] = []

        results: Iterable = connector_service.executer(
            connection=connection, query=self.query
        )

        for operation_names in results:
            list_of_names.append(operation_names[0])

        return list_of_names


operation_service: OperationService = OperationService()
