from typing import List, Any

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query = """
            SELECT indeks as id, raport as orderName
            FROM Stanowiska
        """
        stanowiska_data = connector_service.executer(
            connection=connection, query=stanowiska_query
        )

        result_list = []

        for row in stanowiska_data:
            operation_id = row[0]
            operation_name = row[1]

            operations_query = """
                SELECT
                    sk.indeks AS id,
                    sk.data AS startTime,
                    sz.indekszlecenia AS orderID,
                    z.zlecenie AS orderName
                FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                WHERE sk.stanowisko = ?
            """

            params = [operation_id]

            if from_date and to_date:
                operations_query += " AND sk.data >= ? AND sk.data <= ?"
                params.extend([from_date, to_date])

            operations_data = connector_service.executer(
                connection=connection, query=operations_query, params=params
            )

            operations_list = []

            if not operations_data:
                continue

            for operation_row in operations_data:
                operation = {
                    "id": operation_row[0],
                    "orderID": operation_row[2],
                    "orderName": operation_row[3].strip(),
                    "date": operation_row[1],
                }
                operations_list.append(operation)

            result = {
                "operationID": operation_id,
                "operationName": operation_name,
                "operations": operations_list,
            }

            result_list.append(result)

        return result_list


services = OrderServices()
