import datetime

from src.MsSqlConnector.connector import connector


class CreateMsSqlRecordsService:
    def __init__(self):
        self.zlecenie = "PRW199234"  # this is the random zlecenia without any skany
        self.indeks_zlecenia = 363992  # this is the zlecenia indeks without any skany

    def create_skany(self, beverage):
        connection = connector.get_database_connection()
        indeks_skany = self._get_max_indeks_skany_table()
        indeks_skany_vs_zlecenia = self._get_max_indeks_skany_vs_zlecenia_table()
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        print("connection: ", connection)
        print("indeks_skany: ", indeks_skany)
        print("indeks_skany_vs_zlecenia: ", indeks_skany_vs_zlecenia)
        print("datetime: ", current_time)

        if not connection:
            return False
        if not indeks_skany:
            indeks_skany = 1

        query_for_skan = """
        INSERT INTO skany (
            Indeks, Archiwum, Data, Del, KodKreskowy, Oscieznica, Pozycja,
            Skrzydlo, srcdoc, Stanowisko, Sztuka, Uzytkownik, Zakonczony,
            Czynnosc, DbWHOkna, Guid, GuidParent, Status, Typ, TypSlupka, ErrIdx
        ) VALUES (
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """

        if beverage == "tea":
            params_for_skan = (
                indeks_skany,
                0,
                current_time,
                0,
                "test data",
                1,
                12,
                2,
                0,
                44,
                1,
                64,
                0,
                14,
                5,
                "test data",
                "test data",
                1,
                2,
                2,
                0,
            )
        else:
            params_for_skan = (
                indeks_skany,
                0,
                current_time,
                0,
                "test data",
                1,
                12,
                2,
                0,
                45,
                1,
                64,
                0,
                14,
                5,
                "test data",
                "test data",
                1,
                2,
                2,
                0,
            )

        query_for_skans_vs_zlecenia = """
        INSERT INTO skany_vs_zlecenia (
            IndeksSkanu, IndeksZlecenia, IndeksDodatka, Duplicated
        ) VALUES (
            ?, ?, ?, ?, ?
        )
        """
        params_for_skans_vs_zlecenia = (
            indeks_skany_vs_zlecenia,
            indeks_skany,
            self.indeks_zlecenia,
            None,
            1,
        )
        try:
            with connection.cursor() as cursor:
                cursor.execute(query_for_skan, params_for_skan)
                print("created skany record")
                cursor.execute(
                    query_for_skans_vs_zlecenia, params_for_skans_vs_zlecenia
                )
                print("created skany vs zlecenia record")
        except Exception as e:
            print("error while executing query:", e)
            return False
        else:
            return True

    def _get_max_indeks_skany_table(self):
        connection = connector.get_database_connection()
        if not connection:
            return False

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(indeks) FROM skany")
            result = cursor.fetchone()[0]
        return result

    def _get_max_indeks_skany_vs_zlecenia_table(self):
        connection = connector.get_database_connection()
        if not connection:
            return False

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(indeks) FROM skany_vs_zlecenia")
            result = cursor.fetchone()[0]
        return result


create_records = CreateMsSqlRecordsService()
