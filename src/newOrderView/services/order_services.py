from typing import List, Any

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_order(self, from_date: str, to_date: str):
        query: str = """
            SELECT
                sk.indeks AS id,
                sk.data AS startTime,
                st.indeks as workplace,
                st.raport AS operationName,
                z.indeks AS orderID,
                z.zlecenie AS orderName
            FROM Skany sk
            JOIN Stanowiska st ON sk.stanowisko = workplace
            JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeks
            JOIN zlecenia z ON sz.indeks = orderID
            WHERE 1=1
        """

        connection: pyodbc.Connection = connector_service.get_database_connection()
        params: List[Any] = []

        if from_date and to_date:
            query += " AND startTime >= ? AND startTime <= ?"
            params.extend([from_date, to_date])

        print(query, params)

        data = connector_service.executer(
            connection=connection,
            query=query,
            params=params,
        )
        print(data)

        result_dict = {
            "operationID": None,
            "operationName": None,
            "operations": []
        }

        for row in data:
            operation = {
                "indeks": row[0],
                "date": row[1],
                "orderID": row[4],
                "orderName": row[5],
            }
            result_dict["operations"].append(operation)
            result_dict["OperationID"] = row[2]
            result_dict["OperationName"] = row[3]

        return result_dict


services = OrderServices()
