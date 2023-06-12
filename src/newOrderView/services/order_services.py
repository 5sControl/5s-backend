from typing import List, Any, Tuple, Dict, Optional
from datetime import datetime, timedelta

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service
from src.OrderView.models import IndexOperations
from src.OrderView.utils import get_skany_video_info
from src.CameraAlgorithms.models import Camera
from src.Reports.models import SkanyReport

from ..utils import add_ms


class OrderServices:
    @staticmethod
    def get_operations(from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query: str = """
            SELECT
                indeks AS id,
                raport AS orderId
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
                    z.zlecenie AS orderId
                FROM Skany sk
                    JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                    JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                WHERE sk.stanowisko = ?
            """

            params: List[Any] = [operation_id]

            if from_date and to_date:
                operations_query += " AND sk.data >= ? AND sk.data <= ?"

                from_date_dt = datetime.strptime(from_date, "%Y-%m-%d")
                from_date_dt = from_date_dt + timedelta(microseconds=1)

                to_date_dt = datetime.strptime(to_date, "%Y-%m-%d")
                to_date_dt = to_date_dt + timedelta(days=1) - timedelta(microseconds=1)

                params.extend([from_date_dt, to_date_dt])

            operations_query += " ORDER BY sk.data"

            operations_data: List[Tuple[Any]] = connector_service.executer(
                connection=connection, query=operations_query, params=params
            )

            operations_list: List[Dict[str, Any]] = []

            if not operations_data:
                continue

            for i in range(len(operations_data)):
                operation_row: Tuple[Any] = operations_data[i]

                id: int = operation_row[0]
                orderId: str = operation_row[3].strip()
                startTime: str = str(operation_row[1])
                endTime: str = (
                    str(operation_row[2]) if i < len(operations_data) - 1 else None
                )

                operation: Dict[str, Any] = {
                    "id": id,
                    "orId": orderId,
                    "sTime": startTime,
                    "eTime": endTime,
                }

                startTime_dt: datetime = add_ms(startTime)
                startTime_unix: int = int(startTime_dt.timestamp())

                if endTime is not None:
                    endTime_dt: datetime = add_ms(endTime)

                    if endTime_dt.date() > startTime_dt.date():
                        endTime_dt = startTime_dt + timedelta(hours=1)
                    else:
                        endTime_dt = endTime_dt or startTime_dt + timedelta(hours=1)

                    endTime_unix: int = int(endTime_dt.timestamp())
                    operation["eTime"] = endTime_unix * 1000

                else:
                    endTime_dt = startTime_dt + timedelta(hours=1)
                    endTime_unix: int = int(endTime_dt.timestamp())
                    operation["eTime"] = endTime_unix * 1000

                operation["sTime"] = startTime_unix * 1000

                operations_list.append(operation)

            result = {
                "oprTypeID": operation_id,
                "oprName": operation_name,
                "oprs": operations_list,
            }

            result_list.append(result)
        return result_list

    @staticmethod
    def get_order(from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: str = """
            SELECT
                DISTINCT z.zlecenie AS orderId
            FROM Zlecenia z
                JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indekszlecenia
                JOIN Skany sk ON sz.indeksskanu = sk.indeks
            WHERE sk.data >= ? AND sk.data <= ?
        """

        from_date_dt = datetime.strptime(from_date, "%Y-%m-%d")
        from_date_dt = from_date_dt + timedelta(microseconds=1)

        to_date_dt = datetime.strptime(to_date, "%Y-%m-%d")
        to_date_dt = to_date_dt + timedelta(days=1) - timedelta(microseconds=1)

        params: List[Any] = [from_date_dt, to_date_dt]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result_list: List[Dict[str, Any]] = []

        for order_row in order_data:
            order: Dict[str, Any] = {
                "orId": order_row[0].strip(),
            }

            result_list.append(order)

        return result_list

    @staticmethod
    def get_order_by_details(operation_id: int) -> Dict[str, Any]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query = """
            WITH Operation AS (
                SELECT
                    sk.data AS operationTime
                FROM Skany sk
                    JOIN Stanowiska st ON sk.stanowisko = st.indeks
                WHERE sk.indeks = ?
            )
            SELECT
                z.indeks AS id,
                z.zlecenie AS orderId,
                st.raport AS operationName,
                u.imie AS firstName,
                u.nazwisko AS lastName,
                CONVERT(VARCHAR(23), op.operationTime, 121) AS startTime,
                CASE
                    WHEN DATEPART(year, sk_next.data) > DATEPART(year, op.operationTime)
                        OR DATEPART(month, sk_next.data) > DATEPART(month, op.operationTime)
                        OR DATEPART(day, sk_next.data) > DATEPART(day, op.operationTime)
                        THEN DATEADD(hour, 1, op.operationTime)
                    ELSE CONVERT(VARCHAR(23), sk_next.data, 121)
                END AS endTime,
                st.indeks AS workplaceID,
                sk.indeks AS operationID,
                z.typ AS type
            FROM Zlecenia z
                JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indekszlecenia
                JOIN Skany sk ON sz.indeksskanu = sk.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
                JOIN Uzytkownicy u ON sk.uzytkownik = u.indeks
                JOIN Operation op ON op.operationTime = sk.data
                LEFT JOIN Skany sk_next ON sk_next.data > op.operationTime
                                        AND sk_next.stanowisko = st.indeks
            WHERE sk.indeks = ?
        """

        params: List[Any] = [operation_id, operation_id]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        if order_data:
            id: int = order_data[0][8]
            orderId: str = order_data[0][1].strip()
            operationName: str = order_data[0][2]
            firstName: str = order_data[0][3]
            lastName: str = order_data[0][4]
            startTime: datetime = datetime.strptime(
                str(order_data[0][5]), "%Y-%m-%d %H:%M:%S.%f"
            )
            endTime_str = str(order_data[0][6]) if order_data[0][6] else None

            if endTime_str:
                if '.' not in endTime_str:
                    endTime_str += '.000'
                endTime = datetime.strptime(endTime_str, "%Y-%m-%d %H:%M:%S.%f")
            else:
                endTime = startTime + timedelta(hours=1)

            workplaceID: int = order_data[0][7]
            elementType = order_data[0][9]
            video_data: Optional[Dict[str, Any]] = {"status": False}

            if startTime is not None:
                camera_obj: Optional[Camera] = None
                operation_status: Optional[bool] = None
                video_data: Dict[str, bool] = {}

                skany_report: Optional[SkanyReport] = SkanyReport.objects.filter(
                    skany_index=id
                ).first()
                camera_obj: Optional[Camera] = IndexOperations.objects.filter(
                    type_operation=workplaceID
                ).first()

                if skany_report:
                    operation_status: Optional[bool] = skany_report.violation_found
                    video_time: Optional[bool] = skany_report.start_time

                    if camera_obj and video_time:
                        video_data: Dict[str, Any] = get_skany_video_info(
                            time=(video_time * 1000), camera_ip=camera_obj.camera.id
                        )

            startTime_unix: int = int(startTime.timestamp()) * 1000
            endTime_unix: int = int(endTime.timestamp()) * 1000

            result: Dict[str, Any] = {
                "id": id,
                "orId": orderId,
                "oprName": operationName,
                "elType": elementType,
                "sTime": startTime_unix,
                "eTime": endTime_unix,
                "frsName": firstName,
                "lstName": lastName,
                "status": operation_status,
                "video": video_data,
            }

            return result
        else:
            return {}

    @staticmethod
    def get_whnet_operation() -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        query: str = """
            SELECT
                indeks AS id,
                raport AS operationName
            FROM Stanowiska
        """

        data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=query
        )
        result_list: List[Dict[str, Any]] = []

        for order_row in data:
            order: Dict[str, Any] = {
                "id": int(order_row[0]),
                "operationName": str(order_row[1]).strip(),
            }

            result_list.append(order)

        return result_list
