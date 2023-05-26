from typing import Any, Dict, List, Optional, Tuple
import datetime

import pyodbc

from src.MsSqlConnector.connector import connector as connector_service

from src.Reports.models import SkanyReport


class OrderListService:
    def __init__(
        self,
    ) -> None:
        self.STATUS_TO_FIELD_VALUE = {
            "violation": False,
            "compliance": True,
        }
        self.main_query = """
            SELECT DISTINCT
                z.indeks,
                z.zlecenie,
                CASE
                    WHEN z.zakonczone = '0' AND z.datawejscia IS NOT NULL THEN 'Started'
                    WHEN z.zakonczone = '1' THEN 'Completed'
                    ELSE 'Unknown'
                END AS status,
                z.terminrealizacji,
                z.datawejscia,
                ROW_NUMBER() OVER (PARTITION BY z.zlecenie
                                    ORDER BY CASE WHEN z.zakonczone = '0' THEN 0 ELSE 1 END, z.datawejscia DESC) as rn
            FROM zlecenia z
            WHERE 1=1
        """

        self.skany_index_query = """
            SELECT indeksskanu
            FROM skany_vs_zlecenia
        """

    def get_order_list(
        self,
        search: str,
        order_status: str,
        operation_status: List[str],
        operation_name: List[str],
        from_time: str,
        to_time: str,
    ) -> Optional[List[Dict[str, Dict[str, Any]]]]:
        connection = connector_service.get_database_connection()
        self.extra_qury = " "

        self.extra_qury, params = self._build_query(
            connection=connection,
            search=search,
            order_status=order_status,
            operation_status=operation_status,
            operation_name=operation_name,
            from_time=from_time,
            to_time=to_time,
        )

        results = connector_service.executer(
            connection=connection,
            query=self.main_query + self.extra_qury,
            params=params,
        )

        orders_dict = self._build_orders_dict(results)
        orders_list = list(orders_dict.values())

        for order in orders_list:
            order['datawejscia'] = datetime.strptime(order['datawejscia'], '%Y-%m-%d %H:%M:%S')
        orders_list = sorted(orders_list, key=lambda x: x['datawejscia'])

        print(orders_list)
        return orders_list

    def _build_query(
        self,
        connection: pyodbc.Connection,
        search: str,
        order_status: str,
        operation_status: List[str],
        operation_name: List[str],
        from_time: str,
        to_time: str,
    ) -> Tuple[str, tuple]:
        params = []

        if search:
            self.extra_qury += " AND z.zlecenie LIKE ?"
            params.append(f"%{search}%")

        if order_status is not None:
            if order_status == "completed":
                self.extra_qury += " AND z.zakonczone = 1"
            elif order_status == "started":
                self.extra_qury += " AND z.zakonczone = 0"

        if operation_status != []:
            skanys = self.get_skany_indeks_from_report(operation_status)
            if skanys:
                zlecenie = self.get_zlecenie_indeks_by_skany_indeks(connection, skanys)
                if zlecenie:
                    self.extra_qury += " AND z.zlecenie IN ({})".format(
                        ", ".join([f"'{z}'" for z in zlecenie])
                    )
                else:
                    self.extra_qury += " AND z.zlecenie = 'Not-Found-Data'"
            else:
                self.extra_qury += " AND z.zlecenie = 'Not-Found-Data'"

        if operation_name != []:
            zlecenie_by_stanowisko = self.get_zlecenie_by_operation_names(
                connection, operation_name
            )
            if zlecenie_by_stanowisko:
                self.extra_qury += " AND z.zlecenie IN ({})".format(
                    ", ".join([f"'{z_by_s}'" for z_by_s in zlecenie_by_stanowisko])
                )
            else:
                self.extra_qury += " AND z.zlecenie = 'Not-Found-Data'"

        if from_time and to_time:
            if from_time == to_time:
                self.extra_qury += " AND CAST(datawejscia AS DATE) = ?"
                params.append(from_time)
            else:
                self.extra_qury += " AND z.datawejscia BETWEEN ? AND ?"
                params.extend([from_time, to_time])

        self.extra_qury += " ORDER BY z.zlecenie DESC"

        return self.extra_qury, tuple(params)

    def _build_orders_dict(
        self, results: List[Tuple[str, ...]]
    ) -> Dict[str, Dict[str, Any]]:
        orders_dict = {}

        for result in results:
            zlecenie = result[1]
            if zlecenie not in orders_dict:
                orders_dict[zlecenie] = {
                    "indeks": result[0],
                    "zlecenie": zlecenie,
                    "status": result[2],
                    "terminrealizacji": result[3],
                    "datawejscia": result[4]
                }
            else:
                orders_dict[zlecenie]["indeks"] = result[0]
                orders_dict[zlecenie]["status"] = result[2]
                orders_dict[zlecenie]["terminrealizacji"] = result[3]
                orders_dict[zlecenie]["datawejscia"] = result[4]

        return orders_dict

    def get_zlecenie_indeks_by_skany_indeks(
        self, connection: pyodbc.Connection, skany_list: List[int]
    ) -> List[str]:
        zlecenia_indeks_list = []

        skany_indeks = ",".join(str(indeks) for indeks in skany_list)
        query_zl_indeks = f"""
            SELECT DISTINCT indekszlecenia
            FROM skany_vs_zlecenia
            WHERE indeksskanu IN ({skany_indeks})
        """
        fetched = connector_service.executer(
            connection=connection, query=query_zl_indeks
        )
        zlecenia_indeks_list = [result[0] for result in fetched]

        if zlecenia_indeks_list:
            zlecenie_indeks = ",".join(str(indeks) for indeks in zlecenia_indeks_list)
        else:
            zlecenie_indeks = "nothing, was founded"
        query_zl = f"""
            SELECT DISTINCT zlecenie
            FROM zlecenia
            WHERE indeks IN ({zlecenie_indeks})
        """
        fetched = connector_service.executer(connection=connection, query=query_zl)
        zlecenie_list = [result[0] for result in fetched]

        return zlecenie_list

    def get_all_skany_indeks(self) -> List[int]:
        connection = connector_service.get_database_connection()

        fetched = connector_service.executer(
            connection=connection, query=self.skany_index_query
        )
        indeks_skany = [result[0] for result in fetched]

        return indeks_skany

    def get_skany_indeks_from_report(self, statuses: List[str]) -> List[int]:
        status_set = set(statuses) - set(["no data"])

        skany_indexes = list(
            SkanyReport.objects.filter(
                report__violation_found__in=[
                    self.STATUS_TO_FIELD_VALUE[status] for status in status_set
                ]
            ).values_list("skany_index", flat=True)
        )

        if "no data" in statuses:
            all_skany_indeks = self.get_all_skany_indeks()
            skany_indexes += all_skany_indeks

        return skany_indexes

    def get_zlecenie_by_operation_names(
        self, connection: pyodbc.Connection, operation_names: List[str]
    ) -> List[str]:
        zlecenie = []

        query = """
            SELECT DISTINCT zlecenia.zlecenie
            FROM Stanowiska
            INNER JOIN Skany ON Stanowiska.indeks = Skany.stanowisko
            INNER JOIN Skany_vs_Zlecenia ON Skany.indeks = Skany_vs_Zlecenia.indeksskanu
            INNER JOIN zlecenia ON Skany_vs_Zlecenia.indekszlecenia = zlecenia.indeks
            WHERE Stanowiska.raport IN ({})
        """.format(
            ", ".join([f"'{op_name}'" for op_name in operation_names])
        )

        results = connector_service.executer(connection=connection, query=query)

        for indeks_zlecenie in results:
            zlecenie.append(indeks_zlecenie[0])

        return zlecenie


order_list_service = OrderListService()
