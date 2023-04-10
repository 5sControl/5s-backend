from src.MsSqlConnector.connector import connector


class MsSqlConnector:
    def get_max_skany_indeks_by_stanowisko(self, stanowisko):
        connection = connector.get_database_connection()
        if not connection:
            return False

        connection = connector.get_database_connection()

        with connection.cursor() as cursor:
            cursor.execute("SELECT MAX(indeks) FROM skany WHERE stanowisko = ?", (stanowisko,))
            result = cursor.fetchone()[0]
        return result


create_records = MsSqlConnector()
