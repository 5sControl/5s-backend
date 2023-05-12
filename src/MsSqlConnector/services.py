from src.Core.exceptions import DatabaseConnectioneError
from src.MsSqlConnector.connector import connector


class MsSqlConnector:
    def operation_control_data(self, stanowisko: int):
        connection = connector.get_database_connection()
        if not connection:
            raise DatabaseConnectioneError("get_max_skany_indeks_by_stanowisko")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT MAX(Skany.indeks), Zlecenia.Zlecenie, Zlecenia.DataWejscia
                FROM Skany
                JOIN Skany_vs_Zlecenia ON Skany.indeks = Skany_vs_Zlecenia.IndeksSkanu
                JOIN Zlecenia ON Skany_vs_Zlecenia.IndeksZlecenia = Zlecenia.Indeks
                WHERE Skany.stanowisko = ?
                GROUP BY Zlecenia.Zlecenie, Zlecenia.DataWejscia
                """, (stanowisko,)
            )

            row = cursor.fetchall()

        print(row)
        result = {
            "skany_index": row[0],
            "zlecenie": row[1],
            "execution_date": row[2],
        }

        return result


create_records = MsSqlConnector()
