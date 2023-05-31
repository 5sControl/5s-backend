from typing import List, Any, Tuple, Dict

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        query: str = """
            SELECT
                sk.indeks AS id,
                sk.data AS startTime,
                st.indeks as workplace,
                st.raport AS operationName
            FROM skany sk
            JOIN Stanowiska st ON sk.stanowisko = st.indeks
            WHERE 1=1
        """

        connection: pyodbc.Connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
            query += " AND sk.data >= ? AND sk.data <= ?"
            params.extend([from_date, to_date])

        print(query, params)

        data = connector_service.executer(
            connection=connection,
            query=query,
            params=params,
        )
        result_dict = {
            "OperationID": None,
            "OperationName": None,
            "operations": []
        }

        for row in data:
            operation = {
                "indeks": row[0],
                "data": row[1]
            }
            result_dict["operations"].append(operation)
            result_dict["OperationID"] = row[2]
            result_dict["OperationName"] = row[3]

        return result_dict

services = OrderServices()
