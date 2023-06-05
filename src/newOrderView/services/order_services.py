from typing import List, Any, Tuple, Dict, Optional
from datetime import datetime, timedelta, timezone

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service
from src.OrderView.models import IndexOperations
from src.OrderView.utils import get_skany_video_info
from src.CameraAlgorithms.models import Camera
from src.Reports.models import SkanyReport

from ..utils import add_ms


class OrderServices:
    def get_operations(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query: str = """
            SELECT
                indeks AS id,
                raport AS orderName
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
                    z.zlecenie AS orderName
                FROM Skany sk
                    JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                    JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                WHERE sk.stanowisko = ?
            """

            params: List[Any] = [operation_id]

            if from_date and to_date:
                operations_query += " AND sk.data >= ? AND sk.data <= ?"
                to_date = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1)
                params.extend([from_date, to_date])
                params[1] = to_date

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
                orderName: str = operation_row[3].strip()
                startTime: str = str(operation_row[1])
                endTime: str = (
                    str(operation_row[2]) if i < len(operations_data) - 1 else None
                )

                operation: Dict[str, Any] = {
                    "id": id,
                    "orderName": orderName,
                    "startTime": startTime,
                    "endTime": endTime,
                }

                startTime: datetime = add_ms(startTime)
                if endTime is not None:
                    endTime: datetime = add_ms(endTime)

                    if endTime and endTime.date() > startTime.date():
                        endTime = startTime + timedelta(hours=1)
                    else:
                        endTime = endTime or startTime + timedelta(hours=1)

                    operation["endTime"] = endTime.strftime("%Y-%m-%d %H:%M:%S.%f")
                else:
                    endTime = startTime + timedelta(hours=1)

                    operation["endTime"] = endTime.strftime("%Y-%m-%d %H:%M:%S.%f")

                operations_list.append(operation)

            result = {
                "operationID": operation_id,
                "operationName": operation_name,
                "operations": operations_list,
            }

            result_list.append(result)

        return result_list

    def get_order(self, from_date: str, to_date: str) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: str = """
            SELECT
                DISTINCT z.zlecenie AS orderName
            FROM Zlecenia z
                JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indekszlecenia
                JOIN Skany sk ON sz.indeksskanu = sk.indeks
            WHERE sk.data >= ? AND sk.data <= ?
        """

        params: List[Any] = [from_date, to_date]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result_list: List[Dict[str, Any]] = []

        for order_row in order_data:
            order: Dict[str, Any] = {
                "orderName": order_row[0].strip(),
            }

            result_list.append(order)

        
        print(f"From date {from_date} - to date {to_date}")
        return result_list

    def get_order_by_details(self, operation_id: int) -> Dict[str, Any]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: str = """
            WITH Operation AS (
                SELECT
                    sk.data AS operationTime
                FROM Skany sk
                    JOIN Stanowiska st ON sk.stanowisko = st.indeks
                WHERE sk.indeks = ?
            )
            SELECT
                z.indeks AS id,
                z.zlecenie AS orderName,
                st.raport AS operationName,
                u.imie AS firstName,
                u.nazwisko AS lastName,
                op.operationTime AS startTime,
                (
                    SELECT MIN(sk_next.data)
                    FROM Skany sk_next
                    WHERE sk_next.data > op.operationTime
                        AND sk_next.stanowisko = st.indeks
                ) AS endTime,
                st.indeks AS workplaceID,
                sk.indeks AS operationID
            FROM Zlecenia z
                JOIN Skany_vs_Zlecenia sz ON z.indeks = sz.indekszlecenia
                JOIN Skany sk ON sz.indeksskanu = sk.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
                JOIN Uzytkownicy u ON sk.uzytkownik = u.indeks
                JOIN Operation op ON op.operationTime = sk.data
            WHERE sk.indeks = ?
        """

        params: List[Any] = [operation_id, operation_id]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        if order_data:
            id: int = order_data[0][8]
            orderName: str = order_data[0][1].strip()
            operationName: str = order_data[0][2]
            firstName: str = order_data[0][3]
            lastName: str = order_data[0][4]
            startTime: str = str(order_data[0][5])
            endTime: str = order_data[0][6]
            workplaceID: int = order_data[0][7]
            video_data: Optional[Dict[str, Any]] = {"status": False}

            if startTime is not None:
                camera_obj: Optional[Camera] = None

                time: datetime = add_ms(startTime)
                time_utc: datetime = time.replace(tzinfo=timezone.utc)

                try:
                    camera_obj: Camera = IndexOperations.objects.get(
                        type_operation=workplaceID
                    ).camera
                except IndexOperations.DoesNotExist:
                    pass

                if not camera_obj:
                    video_data: Dict[str, bool] = {"status": False}
                else:
                    video_data: Dict[str, Any] = get_skany_video_info(
                        time=time_utc.isoformat(), camera_ip=camera_obj.id
                    )

                skany_report: Optional[SkanyReport] = SkanyReport.objects.filter(
                    skany_index=id
                ).first()
                print(skany_report, id)
                if skany_report:
                    operation_status: Optional[bool] = skany_report.violation_found
                else:
                    operation_status: Optional[bool] = None

            result: Dict[str, Any] = {
                "id": id,
                "orderName": orderName,
                "operationName": operationName,
                "startTime": startTime,
                "endTime": endTime,
                "firstName": firstName,
                "lastName": lastName,
                "status": operation_status,
                "video_data": video_data,
            }

            return result
        else:
            return {}


services = OrderServices()
