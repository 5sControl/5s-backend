from typing import List, Any, Tuple, Dict

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        query: str = '''
            SELECT sk.indeks, sk.data, st.OperationID, st.OperationName
            FROM skany sk
            JOIN Stanowiska st ON sk.stanowisko = st.indeks
            WHERE 1=1
        '''

        connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
            query += " AND sk.data >= ? AND sk.data <= ?"
            params.extend([from_date, to_date])

        print(query, params)

        results = connector_service.executer(
            connection=connection,
            query=query,
            params=params,
        )
        print(results)
        return results


services = OrderServices()

