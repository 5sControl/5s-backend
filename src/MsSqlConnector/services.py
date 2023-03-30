import datetime
from random import choice

from src.MsSqlConnector.connector import connector


class CreateMsSqlRecordsService:
    # 128 - eLang
    # 144 - 5S Control
    # 145 - Manifest
    # 132 - healthUapp
    def __init__(self):
        self.zlecenie_and_indeks = {"PRW199234": 363992, "PRW199235": 364570, "PRW199236": 364571}
        self.indeks_zlecenia = [363992, 364570, 364571]

    def create_skany(self, beverage, worker):
        connection = connector.get_database_connection()
        indeks_skany = self._get_max_indeks_skany_table()
        indeks_skany_vs_zlecenia = self._get_max_indeks_skany_vs_zlecenia_table()
        now = datetime.datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

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
            raport = 44
        elif beverage == "coffee":
            raport = 45
        elif beverage == "water":
            raport = 46
        elif beverage == "milk":
            raport = 47

        if worker == "elang":
            imie_nazwisko = 128
        elif worker == "5s control":
            imie_nazwisko = 144
        elif worker == "manifest":
            imie_nazwisko = 145
        elif worker == "healthuapp":
            imie_nazwisko = 132

        print(beverage)
        print(imie_nazwisko)

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
            raport,
            1,
            imie_nazwisko,
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

        random_choice_zlecenia = choice(self.indeks_zlecenia)
        query_for_skans_vs_zlecenia = """
        INSERT INTO skany_vs_zlecenia (
            Indeks, IndeksSkanu, IndeksZlecenia, IndeksDodatka, Duplicated
        ) VALUES (
            ?, ?, ?, ?, ?
        )
        """
        params_for_skans_vs_zlecenia = (
            indeks_skany_vs_zlecenia,
            indeks_skany,
            random_choice_zlecenia,
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

    def get_max_skany_indeks_by_typ(self, typ):
        connection = connector.get_database_connection()
        if not connection:
            return False

        connection = connector.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(indeks) FROM skany WHERE typ = ?", (typ,))
            result = cursor.fetchone()[0]
        return result

    def _get_max_indeks_skany_table(self):
        connection = connector.get_database_connection()
        if not connection:
            return False

        connection = connector.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(indeks) FROM skany")
            result = cursor.fetchone()[0]
        return result + 1

    def _get_max_indeks_skany_vs_zlecenia_table(self):
        connection = connector.get_database_connection()
        if not connection:
            return False

        connection = connector.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(indeks) FROM skany_vs_zlecenia")
            result = cursor.fetchone()[0]
        return result + 1


create_records = CreateMsSqlRecordsService()
