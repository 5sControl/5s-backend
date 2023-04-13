from src.MsSqlConnector.connector import connector as connector_service

from src.Reports.models import SkanyReport


class OrderListService:
    def __init__(self,):
        self.STATUS_TO_FIELD_VALUE = {
            "violation": False,
            "compliance": True,
        }

    def get_order_list(
        self,
        search=None,
        order_status=None,
        operation_status=None,
        operation_name=None,
        from_time=None,
        to_time=None,
    ):
        connection = connector_service.get_database_connection()

        with connection.cursor() as cursor:
            query, params = self._build_query(
                search=search,
                order_status=order_status,
                operation_status=operation_status,
                operation_name=operation_name,
                from_time=from_time,
                to_time=to_time,
            )

            print(query, params)
            cursor.execute(query, params)
            results = cursor.fetchall()

        orders_dict = self._build_orders_dict(results)
        orders_list = list(orders_dict.values())
        return orders_list

    def _build_query(self, search, order_status, operation_status, operation_name, from_time, to_time):
        query = """
            SELECT DISTINCT
                z.indeks,
                z.zlecenie,
                CASE
                    WHEN z.zakonczone = '0' AND z.datawejscia IS NOT NULL THEN 'Started'
                    WHEN z.zakonczone = '1' THEN 'Completed'
                    ELSE 'Unknown'
                END AS status,
                z.terminrealizacji,
                ROW_NUMBER() OVER (PARTITION BY z.zlecenie
                                    ORDER BY CASE WHEN z.zakonczone = '0' THEN 0 ELSE 1 END, z.datawejscia DESC) as rn
            FROM zlecenia z
            WHERE 1=1
        """

        params = []

        if search:
            query += " AND z.zlecenie LIKE ?"
            params.append(f"%{search}%")

        if order_status is not None:
            if order_status == "completed":
                query += " AND z.zakonczone = 1"
            elif order_status == "started":
                query += " AND z.zakonczone = 0"

        if operation_status != []:
            skanys = self.get_skany_indeks_from_report(operation_status)
            if skanys:
                zlecenie = self.get_zlecenie_indeks_by_skany_indeks(skanys)
                if zlecenie:
                    query += " AND z.zlecenie IN ({})".format(
                        ", ".join([f"'{z}'" for z in zlecenie])
                    )
                else:
                    query += " AND z.zlecenie = 'Not-Found-Data'"
            else:
                query += " AND z.zlecenie = 'Not-Found-Data'"

        if operation_name != []:
            zlecenie_by_stanowisko = self.get_zlecenie_by_operation_names(
                operation_name
            )
            if zlecenie_by_stanowisko:
                query += " AND z.zlecenie IN ({})".format(
                    ", ".join([f"'{z_by_s}'" for z_by_s in zlecenie_by_stanowisko])
                )
            else:
                query += " AND z.zlecenie = 'Not-Found-Data'"

        if from_time and to_time:
            if from_time != to_time:
                query += " AND z.terminrealizacji BETWEEN ? AND ?"
                params.extend([from_time, to_time])
            else:
                query += " AND z.terminrealizacji = ?"
                params.append(from_time)

        query += " ORDER BY z.zlecenie DESC"

        return query, tuple(params)

    def _build_orders_dict(self, results):
        orders_dict = {}
        for result in results:
            zlecenie = result[1]
            if zlecenie not in orders_dict:
                orders_dict[zlecenie] = {
                    "indeks": result[0],
                    "zlecenie": zlecenie,
                    "status": result[2],
                    "terminrealizacji": result[3],
                }
            else:
                orders_dict[zlecenie]["indeks"] = result[0]
                orders_dict[zlecenie]["status"] = result[2]
                orders_dict[zlecenie]["terminrealizacji"] = result[3]
        return orders_dict

    def get_zlecenie_indeks_by_skany_indeks(self, skany_list):
        zlecenia_indeks_list = []

        connection = connector_service.get_database_connection()

        skany_indeks = ",".join(str(indeks) for indeks in skany_list)
        query_zl_indeks = f"""
            SELECT DISTINCT indekszlecenia
            FROM skany_vs_zlecenia
            WHERE indeksskanu IN ({skany_indeks})
        """

        with connection.cursor() as cursor:
            cursor.execute(query_zl_indeks)
            zlecenia_indeks_list = [result[0] for result in cursor.fetchall()]

        if zlecenia_indeks_list:
            zlecenie_indeks = ",".join(str(indeks) for indeks in zlecenia_indeks_list)
        else:
            zlecenie_indeks = "nothing, was founded"
        query_zl = f"""
            SELECT DISTINCT zlecenie
            FROM zlecenia
            WHERE indeks IN ({zlecenie_indeks})
        """

        with connection.cursor() as cursor:
            cursor.execute(query_zl)
            zlecenie_list = [result[0] for result in cursor.fetchall()]

        return zlecenie_list

    def get_all_skany_indeks(self):
        connection = connector_service.get_database_connection()
        query = """
            SELECT indeksskanu
            FROM skany_vs_zlecenia
        """
        with connection.cursor() as cursor:
            cursor.execute(query)
            indeks_skany = [result[0] for result in cursor.fetchall()]
        return indeks_skany

    def get_skany_indeks_from_report(self, statuses):
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

    def get_zlecenie_by_operation_names(self, operation_names):
        connection = connector_service.get_database_connection()

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

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        for indeks_zlecenie in results:
            zlecenie.append(indeks_zlecenie[0])

        return zlecenie


order_list_service = OrderListService()
