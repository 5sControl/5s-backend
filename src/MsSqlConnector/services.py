import logging

from src.Core.exceptions import DatabaseConnectioneError
from src.MsSqlConnector.connector import connector

logger = logging.getLogger(__name__)


class MsSqlConnector:
    def operation_control_data(self, stanowisko: int):
        connection = connector.get_database_connection()
        if not connection:
            raise DatabaseConnectioneError("operation_control_data")

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    MAX(Skany.indeks),
                    Zlecenia.Zlecenie,
                    Zlecenia.DataWejscia
                FROM Skany
                JOIN Skany_vs_Zlecenia ON Skany.indeks = Skany_vs_Zlecenia.IndeksSkanu
                JOIN Zlecenia ON Skany_vs_Zlecenia.IndeksZlecenia = Zlecenia.Indeks
                WHERE Skany.stanowisko = ?
                GROUP BY Zlecenia.Zlecenie, Zlecenia.DataWejscia
                """, (stanowisko,)
            )

            row = cursor.fetchall()[0]
            logger.warning(f"data for operation control: {row}")
        
        result = {
            "skany_index": row[0],
            "zlecenie": row[1],
            "execution_date": row[2],
        }

        return result


create_records = MsSqlConnector()
