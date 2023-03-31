from datetime import datetime, timezone
from collections import defaultdict

from src.MsSqlConnector.connector import connector as connector_service
from src.Reports.models import Report


class OrderService:
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

    def get_order_list(self, search=None, status=None):
        if search:
            results = self._filtered_orders_list(search)
            orders_list = [
                {
                    "indeks": result[3],
                    "zlecenie": result[0],
                    "status": result[1],
                    "terminrealizacji": result[2]
                } for result in results
            ]
        else:
            results = self._get_all_list_of_orders()
            if status == 1:
                orders_list = [
                    {
                        "indeks": result[0],
                        "zlecenie": result[1],
                        "status": result[2],
                        "terminrealizacji": result[3]
                    } for result in results if result[2] == "Completed"
                ]
            elif status == 0:
                orders_list = [
                    {
                        "indeks": result[0],
                        "zlecenie": result[1],
                        "status": result[2],
                        "terminrealizacji": result[3]
                    } for result in results if result[2] == "Started"
                ]
            else:
                orders_list = [
                    {
                        "indeks": result[0],
                        "zlecenie": result[1],
                        "status": result[2],
                        "terminrealizacji": result[3]
                    } for result in results
                ]

        return orders_list

    def _filtered_orders_list(self, zlecenie_id):
        connection = connector_service.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT DISTINCT
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
                WHERE z.zlecenie LIKE ?
                """,
                (f"{zlecenie_id}%",),
            )
            results = cursor.fetchall()
        return results

    def _get_all_list_of_orders(self):
        connection = connector_service.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT *
                    FROM (
                        SELECT z.indeks,
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
                    ) as subquery
                    WHERE rn = 1
                    """
            )
            results = cursor.fetchall()
        return results

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
                    reports = Report.objects.filter(algorithm__name='operation_control').values()
                    status = None
                    for report in reports:
                        try:
                            if report["extra"]["skany_index"] == row[0]:
                                status = report["violation_found"]
                        except (KeyError, TypeError):
                            continue
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


orderView_service = OrderService()
