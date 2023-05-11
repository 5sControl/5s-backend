from src.Core.exceptions import DatabaseConnectioneError
from src.MsSqlConnector.connector import connector


class MsSqlConnector:
    def extra_data(self, stanowisko: int):
        connection = connector.get_database_connection()
        if not connection:
            raise DatabaseConnectioneError("get_max_skany_indeks_by_stanowisko")

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT MAX(s.indeks), z.IndeksZlecenia, z.DataWejscia "
                "FROM skany s "
                "JOIN Skany_vs_Zlecenia svz ON s.Indeks = svz.IndeksSkanu "
                "JOIN Zlecenia z ON z.Indeks = svz.IndeksZlecenia "
                "WHERE s.stanowisko = ?",
                (stanowisko,)
            )
            row = cursor.fetchone()

        result = {
            "skany_index": row[0],
            "zlecenia_index": row[1],
            "execution_date": row[2],
        }

        return result


create_records = MsSqlConnector()
