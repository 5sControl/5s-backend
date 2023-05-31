from typing import List, Any, Tuple, Dict

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_zlecenie(self, from_date: str, to_date: str):
        zlecenie_query = """
                SELECT z.indeks as id, z.zlecenie
                FROM zlecenia z
                WHERE 1=1
            """

        connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
            if from_date == to_date:
                zlecenie_query += " AND CAST(datawejscia AS DATE) = ?"
                params.append(from_date)
            else:
                zlecenie_query += " AND z.datawejscia BETWEEN ? AND ?"
                params.extend([from_date, to_date])

        data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=zlecenie_query, params=params
        )

        result: List[Dict[str, Any]] = [
            {"id": item[0], "zlecenie": item[1].strip()} for item in data
        ]

        return result


services = OrderServices()
