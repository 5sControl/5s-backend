from typing import List, Any

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def __init__(self) -> None:
        self.zlecenie_query = """
                SELECT z.indeks as id, z.zlecenie
                FROM zlecenia z
                WHERE 1=1
            """

    def get_zlecenie(self, from_date: str, to_date: str):
        connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
            if from_date == to_date:
                self.zlecenie_query += " AND CAST(datawejscia AS DATE) = ?"
                params.append(from_date)
            else:
                self.zlecenie_query += " AND z.datawejscia BETWEEN ? AND ?"
                params.extend([from_date, to_date])

        results = connector_service.executer(connection=connection, query=self.zlecenie_query)

        print(results)


services: OrderServices = OrderServices()
