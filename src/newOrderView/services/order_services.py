from typing import List, Any, Tuple, Dict
from datetime import datetime, timedelta

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service


class OrderServices:
    def get_operations(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query: str = """
            SELECT indeks, raport
            FROM Stanowiska
        """

        stanowiska_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=stanowiska_query
        )

        result_list: List[Dict[str, Any]] = []

        for row in stanowiska_data:
            operation_id: int = row[0]
            operation_name: str = row[1]

            operations_query: str = """
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

            operations_data: List[Tuple[Any]] = connector_service.executer(
                connection=connection, query=operations_query, params=params
            )

            operations_list: List = []

            if not operations_data:
                continue

            for i in range(len(operations_data)):
                operation_row: Tuple[Any] = operations_data[i]
                operation = {
                    "indeks": operation_row[0],
                    "orderID": operation_row[3],
                    "orderName": operation_row[4].strip(),
                    "startTime": operation_row[1],
                    "endTime": operation_row[2]
                    if i < len(operations_data) - 1
                    else None,
                }

                if operation["endTime"] is None:
                    startTime: datetime = datetime.strptime(operation["startTime"], "%Y-%m-%d %H:%M:%S.%f")
                    endTime: datetime = startTime + timedelta(hours=1)
                    max_end_time: datetime = endTime.replace(hour=17, minute=0, second=0, microsecond=0)
                    if endTime > max_end_time:
                        operation["endTime"]: datetime = max_end_time.strftime("%Y-%m-%d %H:%M:%S.%f")
                    else:
                        operation["endTime"]: datetime = endTime.strftime("%Y-%m-%d %H:%M:%S.%f")

                operations_list.append(operation)

            result = {
                "operationID": operation_id,
                "operationName": operation_name,
                "operations": operations_list,
            }

            result_list.append(result)

        return result_list

    def get_order(self, from_date: str, to_date: str):
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: str = """
            SELECT z.indeks AS id, z.zlecenie AS orderName
            FROM Zlecenia z
            JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indekszlecenia
            JOIN Skany sk ON sz.indeksskanu = sk.indeks
            WHERE sk.data >= ? AND sk.data <= ?
        """

        params = [from_date, to_date]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result_list: List[Dict[str, Any]] = []

        for order_row in order_data:
            order: Dict[str, Any] = {
                "id": order_row[0],
                "orderName": order_row[1].strip(),
            }

            result_list.append(order)

        return result_list

    def get_order_by_details(self, operation_id: int):
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: str = """
            SELECT z.indeks AS id, z.zlecenie AS orderName, st.raport AS raport, u.imie AS firstName, u.nazwisko AS lastName
            FROM Zlecenia z
            JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indkeszlecenia
            JOIN Skany sk ON sz.indeksskanu = sk.indeks
            JOIN Skanowiska st ON sk.stanowisko = st.indeks
            JOIN Uzytkownicy u ON sk.uzytkownik = u.indeks
            WHERE sk.indeks = ?
        """

        params = [operation_id]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result_list: List[Dict[str, Any]] = []

        for order_row in order_data:
            order: Dict[str, Any] = {
                "id": order_row[0],
                "orderName": order_row[1].strip(),
                "operationName": order_row[2],
                "firstName": order_row[3],
                "lastName": order_row[4]
            }

            result_list.append(order)

        return result_list


services = OrderServices()
