from collections import defaultdict
from typing import List, Any, Tuple, Dict, Optional
from datetime import datetime, timedelta
import logging

import pyodbc

from src.Core.types import Query
from src.MsSqlConnector.connector import connector as connector_service
from src.CameraAlgorithms.models import Camera
from src.Reports.models import SkanyReport
from src.OrderView.models import IndexOperations
from src.OrderView.utils import get_skany_video_info
from src.newOrderView.utils import (
    add_ms,
    convert_to_gmt0,
    convert_to_unix,
    calculate_duration,
)

logger = logging.getLogger(__name__)


class OrderServices:
    @staticmethod
    def get_order(
        from_date: str, to_date: str, operation_type_ids: List[int]
    ) -> List[Dict[str, Any]]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_query: Query = """
            SELECT
                sk.indeks AS id,
                z.zlecenie AS orderId,
                sk.data AS startTime,
                LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
            WHERE sk.data >= ? AND sk.data <= ?
        """

        if operation_type_ids:
            order_query += " AND st.indeks IN ({})" "".format(
                ",".join(str(id) for id in operation_type_ids)
            )

        if from_date and to_date:
            from_date_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d")
            from_date_dt: datetime = from_date_dt + timedelta(microseconds=1)

            to_date_dt: datetime = datetime.strptime(to_date, "%Y-%m-%d")
            to_date_dt: datetime = (
                to_date_dt + timedelta(days=1) - timedelta(microseconds=1)
            )

        params: List[Any] = [from_date_dt, to_date_dt]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_query, params=params
        )

        result_dict: Dict[str, int] = defaultdict(int)

        for order_row in order_data:
            order_id: str = order_row[1].strip()
            startTime: datetime = order_row[2]
            endTime: Optional[datetime] = order_row[3]

            if endTime is not None:
                if endTime.date() > startTime.date():
                    endTime: datetime = startTime + timedelta(hours=1)
                else:
                    endTime: datetime = endTime or startTime + timedelta(hours=1)

            else:
                endTime: datetime = startTime + timedelta(hours=1)

            duration: int = calculate_duration(startTime, endTime)

            result_dict[order_id] += duration

        result_list: List[Dict[str, Any]] = [
            {"orId": order_id, "duration": duration}
            for order_id, duration in result_dict.items()
        ]

        return result_list

    @staticmethod
    def get_order_by_details(operation_id: int) -> Dict[str, Any]:
        connection: pyodbc.Connection = connector_service.get_database_connection()

        order_detail_query: Query = """
            SELECT
                sk.indeks AS id,
                sk.data AS startTime,
                LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime,
                z.zlecenie AS orderId,
                z.typ AS type,
                st.raport AS operationName,
                st.indeks AS workplaceID,
                u.imie AS firstName,
                u.nazwisko AS lastName
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
                JOIN Uzytkownicy u ON sk.uzytkownik = u.indeks
            WHERE sk.indeks = ?
        """

        params: List[Any] = [operation_id]

        order_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=order_detail_query, params=params
        )

        if order_data:
            id: int = order_data[0][0]
            startTime: str = str(
                order_data[0][1]
            )  # FIXME -> whithout transform datetime to str
            endTime: str = str(order_data[0][2]) if order_data is not None else None
            orderId: str = str(order_data[0][3]).strip()
            elementType: str = order_data[0][4]
            operationName: str = order_data[0][5]
            workplaceID: int = order_data[0][6]
            firstName: str = order_data[0][7]
            lastName: str = order_data[0][8]

            video_data: Optional[Dict[str, Any]] = None

            startTime_dt: datetime = add_ms(startTime)
            startTime_dt: datetime = convert_to_gmt0(startTime_dt)
            startTime_unix: int = convert_to_unix(startTime_dt)

            if endTime is not None:
                endTime_dt: datetime = add_ms(endTime)
                endTime_dt: datetime = convert_to_gmt0(endTime_dt)

                if endTime_dt.date() > startTime_dt.date():
                    endTime_dt: datetime = startTime_dt + timedelta(hours=1)
                else:
                    endTime_dt: datetime = endTime_dt or startTime_dt + timedelta(
                        hours=1
                    )

                endTime_unix: int = convert_to_unix(endTime_dt)
            else:
                endTime_dt = startTime_dt + timedelta(hours=1)
                endTime_unix: int = convert_to_unix(endTime_dt)

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
                        time=(video_time), camera_ip=camera_obj.camera.id
                    )

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
