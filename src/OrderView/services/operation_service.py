from typing import List
from src.MsSqlConnector.connector import connector as connector_service


class OperationService:
    def get_operation_names(self) -> List[str]:
        connection = connector_service.get_database_connection()
        list_of_names = []

        query = """
            SELECT DISTINCT Raport
            FROM Stanowiska
        """

        results = connector_service.executer(connection=connection, query=query)

        for operation_names in results:
            list_of_names.append(operation_names[0])

        return list_of_names


operation_service = OperationService()
