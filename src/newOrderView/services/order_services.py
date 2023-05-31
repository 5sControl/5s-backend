from typing import List, Any
from datetime import datetime

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_operations(self, from_date: str, to_date: str):
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query = """
            SELECT indeks, raport
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
                    LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime,
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

            operations_query += " ORDER BY sk.data"

            operations_data = connector_service.executer(
                connection=connection, query=operations_query, params=params
            )

            operations_list = []

            if not operations_data:
                continue

            date_object = datetime.strptime(to_date, "%Y-%m-%d")
            formatted_date = date_object.strftime("%Y-%m-%d %H:%M:%S.%f")

            for i in range(len(operations_data)):
                operation_row = operations_data[i]
                operation = {
                    "indeks": operation_row[0],
                    "zlecenieID": operation_row[3],
                    "zlecenie": operation_row[4].strip(),
                    "startTime": operation_row[1],
                    "endTime": operation_row[2] if i < len(operations_data) - 1 else formatted_date,
                }

                if operation["endTime"]:
                    end_time = datetime.strptime(operation["endTime"], "%Y-%m-%d %H:%M:%S.%f")
                    max_end_time = end_time.replace(hour=16, minute=0, second=0, microsecond=0)
                    if end_time > max_end_time:
                        operation["endTime"] = max_end_time.strftime("%Y-%m-%d %H:%M:%S.%f")

                operations_list.append(operation)

            result = {
                "OperationID": operation_id,
                "OperationName": operation_name,
                "operations": operations_list,
            }

            result_list.append(result)

        return result_list

    def get_order(self, from_date: str, to_date: str):
        ...


services = OrderServices()
