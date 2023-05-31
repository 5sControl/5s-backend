from typing import List, Any

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query = """
            SELECT indeks
            FROM Stanowiska
        """
        stanowiska_data = connector_service.executer(
            connection=connection, query=stanowiska_query
        )

        result_list = []

        for row in stanowiska_data:
            operation_id = row[0]
            operations_query = """
                SELECT
                    sk.indeks AS id,
                    sk.data AS startTime,
                    st.indeks AS workplace,
                    st.raport AS operationName,
                    z.indeks AS orderID,
                    z.zlecenie AS orderName
                FROM Skany sk
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeks
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                WHERE st.indeks = ?
            """

            params = [operation_id]

            if from_date and to_date:
                operations_query += " AND sk.data >= ? AND sk.data <= ?"
                params.extend([from_date, to_date])

            operations_data = connector_service.executer(
                connection=connection, query=operations_query, params=params
            )

            if not operations_data:
                continue

            operations_list = []

            for operation_row in operations_data:
                operation = {
                    "indeks": operation_row[0],
                    "zlecenieID": operation_row[4],
                    "zlecenie": operation_row[5].strip(),
                    "data": operation_row[1],
                }
                operations_list.append(operation)

            result = {
                "OperationID": operation_id,
                "OperationName": operations_data[0][3],
                "operations": operations_list,
            }

            result_list.append(result)

        return result_list


services = OrderServices()
