from typing import List, Any, Tuple, Dict

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        order_query = """
                SELECT DISTINCT z.zlecenie as order, z.indeks as id
                FROM zlecenia z
                WHERE 1=1
            """

        connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
            if from_date == to_date:
                order_query += " AND CAST(datawejscia AS DATE) = ?"
                params.append(from_date)
            else:
                order_query += " AND z.datawejscia BETWEEN ? AND ?"
                params.extend([from_date, to_date])

        data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result: List[Dict[str, Any]] = [
            {"id": item[0], "order": item[1].strip()} for item in data
        ]

        return result


services = OrderServices()
