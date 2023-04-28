from collections import defaultdict

from datetime import datetime, timezone

from typing import Dict, List, Optional, Tuple

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service
from src.OrderView.models import IndexOperations

from src.OrderView.utils import get_skany_video_info
from src.Reports.models import SkanyReport


class OrderService:
    def __init__(self):
        self.zl_by_zl_query = """
                SELECT z.indeks, z.data, z.zlecenie, z.klient, z.datawejscia, z.datazakonczenia,
                    z.zakonczone, z.typ, z.color AS orderName, z.terminrealizacji,
                    CASE
                        WHEN z.zakonczone = 0 AND z.datawejscia IS NOT NULL THEN 'Started'
                        ELSE 'Completed'
                    END AS status
                FROM zlecenia z
                WHERE z.zlecenie = ?
            """
        self.query = """
                SELECT s.indeks, s.data, s.stanowisko, s.uzytkownik,
                    st.raport, u.imie, u.nazwisko
                FROM Skany s
                JOIN Skany_vs_Zlecenia sz ON s.indeks = sz.indeksskanu
                JOIN Stanowiska st ON s.stanowisko = st.indeks
                JOIN Uzytkownicy u ON s.uzytkownik = u.indeks
                WHERE sz.indekszlecenia = ?
                AND s.data <= CONVERT(datetime, GETUTCDATE())
            """

    def get_order(self, zlecenie_id: str) -> List[Dict[str, List]]:
        connection = connector_service.get_database_connection()
        response = {}
        status = "Completed"
        zlecenia_dict = self.get_zlecenia_query_by_zlecenie(connection, zlecenie_id)

        for zlecenie_obj in zlecenia_dict:
            skany_dict = defaultdict(list)
            skany_ids_added = set()

            if zlecenie_obj["status"] == "Started":
                status = "Started"

            param = (zlecenie_obj["indeks"],)
            results = self.get_results(connection, param)

            skany_dict = self.build_skany_dict(results, skany_ids_added)

            zlecenie_obj = self.add_skans_to_zlecenie_obj(zlecenie_obj, skany_dict)

        response = self.build_response(zlecenia_dict, response, status)
        return [response]

    def get_results(self, connection, param):
        return connector_service.executer(
            connection=connection, query=self.query, params=param
        )

    def build_skany_dict(self, results, skany_ids_added):
        skany_dict = defaultdict(list)
        for row in results:
            print(row)
            operation_status = self._setup_operation_status(row[0])

            if row[1] is not None:
                time_string = str(row[1])
                if "." not in time_string:
                    time_string += ".000000"
                time = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f")

                time_utc = time.replace(tzinfo=timezone.utc)
                video_data = get_skany_video_info(time=time_utc.isoformat(), camera_ip=self._get_camera_ips(row[2]))
            else:
                video_data = {"status": False}

            skany = self.build_skany_dict_item(row, operation_status, video_data)
            formatted_time = skany["date"].strftime("%Y.%m.%d")

            if skany["indeks"] not in skany_ids_added:
                skany_ids_added.add(skany["indeks"])
                skany_dict[formatted_time].append(skany)

        return skany_dict

    def build_skany_dict_item(self, row, operation_status, video_data):
        if row[1] is not None:
            date_string = str(row[1])
            if len(date_string) == 19:
                date_string += ".000"
            date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S.%f").replace(
                tzinfo=timezone.utc
            )
        else:
            date = None

        return {
            "indeks": row[0],
            "date": date,
            "stanowisko": row[2],
            "uzytkownik": row[3],
            "raport": row[4],
            "worker": f"{row[5]} {row[6]}",
            "status": operation_status,
            "video_data": video_data,
        }

    def add_skans_to_zlecenie_obj(self, zlecenie_obj, skany_dict):
        zlecenie_obj["skans"] = []
        for formatted_time, skany_list in skany_dict.items():
            for skany in skany_list:
                zlecenie_obj["skans"].append(skany)
        return zlecenie_obj

    def build_response(self, zlecenia_dict, response, status):
        response["products"] = list(zlecenia_dict)
        response["status"] = status
        response["indeks"] = response["products"][0]["indeks"]
        response["zlecenie"] = response["products"][0]["zlecenie"]
        response["data"] = response["products"][0]["data"]
        response["klient"] = response["products"][0]["klient"]
        response["datawejscia"] = response["products"][0]["datawejscia"]
        response["orderName"] = response["products"][0]["orderName"]
        response["datazakonczenia"] = response["products"][0]["datazakonczenia"]
        response["terminrealizacji"] = response["products"][0]["terminrealizacji"]
        return response

    def _get_camera_ips(self, stanowiska):
        try:
            camera_ip = IndexOperations.objects.get(type_operation=stanowiska).camera
        except IndexOperations.DoesNotExist:
            camera_ip = None

        return camera_ip

    def _setup_operation_status(self, skany_index) -> Optional[bool]:
        skany_report = SkanyReport.objects.filter(skany_index=skany_index).first()

        if not skany_report:
            return None
        operation_status = skany_report.report.violation_found

        return operation_status

    def get_zlecenia_query_by_zlecenie(
        self, connection: pyodbc.Connection, zlecenie_id: str
    ) -> List[Dict]:
        param = (zlecenie_id,)

        results = connector_service.executer(
            connection=connection, query=self.zl_by_zl_query, params=param
        )

        result = self.transform_result(results)
        return result

    def transform_result(self, result: List[Tuple]) -> List[Dict]:
        transformed_result: List = []
        for data in result:
            transformed_result.append(
                {
                    "indeks": data[0],
                    "data": datetime.strptime(
                        data[1].strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"
                    ).replace(tzinfo=timezone.utc)
                    if data[1] is not None
                    else None,
                    "zlecenie": data[2].strip(),
                    "klient": data[3].strip(),
                    "datawejscia": datetime.strptime(
                        data[4].strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"
                    ).replace(tzinfo=timezone.utc)
                    if data[4]
                    else None,
                    "datazakonczenia": datetime.strptime(
                        data[5].strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"
                    ).replace(tzinfo=timezone.utc)
                    if data[5]
                    else None,
                    "zakonczone": data[6],
                    "typ": data[7].strip(),
                    "terminrealizacji": data[9].strip()
                    if isinstance(data[9], str)
                    else data[9],
                    "orderName": None,
                    "status": data[10].strip(),
                }
            )
        return transformed_result


order_service = OrderService()
