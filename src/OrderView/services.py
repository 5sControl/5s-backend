from datetime import datetime, timezone

from collections import defaultdict

from src.MsSqlConnector.connector import connector as connector_service
from src.Reports.models import SkanyReport


class OrderService:
    def __init__(
        self,
    ):
        self.STATUS_TO_FIELD_VALUE = {
            "violation": False,
            "compliance": True,
        }

    def get_skanyQueryByIds(self, ids):
        placeholders = ",".join(["%s" for _ in ids])
        query = """
            SELECT indeks, data, stanowisko, uzytkownik
            FROM Skany
            WHERE indeks IN ({})
        """.format(
            placeholders
        )

        connection = self._get_connection()
        if not connection:
            return False

        with connection.cursor() as cursor:
            cursor.execute(query, ids)
            results = cursor.fetchall()

        skanyQuery = []
        for row in results:
            skanyQuery.append(
                {
                    "indeks": row[0],
                    "data": row[1].replace(tzinfo=timezone.utc),
                    "stanowisko": row[2],
                    "uzytkownik": row[3],
                }
            )

        return skanyQuery

    def get_zlecenia_query_by_zlecenie(self, zlecenie_id):
        connection = connector_service.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT z.indeks, z.data, z.zlecenie, z.klient, z.datawejscia, z.datazakonczenia,
                        z.zakonczone, z.typ, z.color AS orderName, z.terminrealizacji,
                        CASE
                            WHEN z.zakonczone = 0 AND z.datawejscia IS NOT NULL THEN 'Started'
                            ELSE 'Completed'
                        END AS status
                    FROM zlecenia z
                    WHERE z.zlecenie = ?
                """,
                (str(zlecenie_id),),
            )
            results = cursor.fetchall()
        result = self.transform_result(results)
        print("RESULT: ", result)
        return result

    def get_order_list(
        self, search=None, order_status=None, operation_status=None, operation_name=None
    ):
        connection = connector_service.get_database_connection()

        with connection.cursor() as cursor:
            query, params = self._build_query(
                search=search,
                order_status=order_status,
                operation_status=operation_status,
                operation_name=operation_name,
            )
            print("QUERY", query)
            print("PARAMS", params)
            cursor.execute(query, params)
            results = cursor.fetchall()

        orders_dict = self._build_orders_dict(results)
        orders_list = list(orders_dict.values())
        return orders_list

    def _build_query(self, search, order_status, operation_status, operation_name):
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
            params.append(f"{search}%")

        if order_status is not None:
            if order_status == "completed":
                query += " AND z.zakonczone = 1"
            elif order_status == "started":
                query += " AND z.zakonczone = 0"

        if operation_status is not None:
            skanys = self.get_skany_indexes(operation_status)
            print("Skans was founded: ", skanys)
            if skanys:
                zlecenie = self.get_zlecenie_indeks_by_skany_indeks(skanys)
                if zlecenie:
                    query += " AND z.zlecenie = IN ({})".format(
                        ", ".join("?" * len(zlecenie))
                    )
                    for indeks in zlecenie:
                        params.append(f"{indeks}%")
                else:
                    query += " AND z.zlecenie = 'Not-Found-Data'"
            else:
                query += " AND z.zlecenie = 'Not-Found-Data'"

        if operation_name is not None:
            ...

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

    def get_order(self, zlecenie_id):
        response = {}
        status = "Completed"

        zlecenia_dict = self.get_zlecenia_query_by_zlecenie(zlecenie_id)

        for zlecenie_obj in zlecenia_dict:
            print("Zlecenie obj is ", zlecenie_obj)
            skany_dict = defaultdict(list)
            if zlecenie_obj["status"] == "Started":
                status = "Started"

            connection = connector_service.get_database_connection()

            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT s.indeks, s.data, s.stanowisko, s.uzytkownik,
                        st.raport, u.imie, u.nazwisko
                    FROM Skany s
                    JOIN Skany_vs_Zlecenia sz ON s.indeks = sz.indeksskanu
                    JOIN Stanowiska st ON s.stanowisko = st.indeks
                    JOIN Uzytkownicy u ON s.uzytkownik = u.indeks
                    WHERE sz.indekszlecenia = ?
                    AND s.data <= CONVERT(datetime, GETUTCDATE())
                    """,
                    (zlecenie_obj["indeks"],),
                )
                results = cursor.fetchall()

                skany_ids_added = set()
                for row in results:
                    status = None
                    skany_report = SkanyReport.objects.filter(
                        report__algorithm__name="operation_control", skany_index=row[0]
                    ).first()
                    if skany_report:
                        status = skany_report.report.violation_found
                    skany = {
                        "indeks": row[0],
                        "data": row[1].replace(tzinfo=timezone.utc),
                        "stanowisko": row[2],
                        "uzytkownik": row[3],
                        "raport": row[4],
                        "worker": f"{row[5]} {row[6]}",
                        "status": status,
                    }
                    formatted_time = skany["data"].strftime("%Y.%m.%d")
                    if skany["indeks"] not in skany_ids_added:
                        skany_ids_added.add(skany["indeks"])
                        skany_dict[formatted_time].append(skany)

            zlecenie_obj["skans"] = []
            for formatted_time, skany_list in skany_dict.items():
                for skany in skany_list:
                    zlecenie_obj["skans"].append(skany)

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

        return [response]

    def transform_result(self, result):
        transformed_result = []
        for r in result:
            transformed_result.append(
                {
                    "indeks": r[0],
                    "data": datetime.strptime(
                        r[1].strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"
                    ).replace(tzinfo=timezone.utc),
                    "zlecenie": r[2].strip(),
                    "klient": r[3].strip(),
                    "datawejscia": datetime.strptime(
                        r[4].strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"
                    ).replace(tzinfo=timezone.utc)
                    if r[4]
                    else None,
                    "datazakonczenia": datetime.strptime(
                        r[5].strftime("%Y-%m-%d %H:%M:%S.%f"), "%Y-%m-%d %H:%M:%S.%f"
                    ).replace(tzinfo=timezone.utc)
                    if r[5]
                    else None,
                    "zakonczone": r[6],
                    "typ": r[7].strip(),
                    "terminrealizacji": r[9].strip(),
                    "orderName": None,
                    "status": r[10].strip(),
                }
            )
        return transformed_result

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

    def get_skany_indexes(self, statuses):
        status_set = set(statuses) - set(["no data"])
        skany_indexes = list(
            SkanyReport.objects.filter(
                report__violation_found__in=[
                    self.STATUS_TO_FIELD_VALUE[status] for status in status_set
                ]
            ).values_list("skany_index", flat=True)
        )

        if "no data" in statuses:
            all_skany_indeks = orderView_service.get_all_skany_indeks()
            skany_indexes += all_skany_indeks

        return skany_indexes

    def get_operation_names(self):
        connection = connector_service.get_database_connection()

        query = """
            SELECT DISTINCT Raport
            FROM Stanowiska
        """

        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()

        return results


orderView_service = OrderService()
