from datetime import datetime
from typing import Any, List, Tuple
from src.Core.types import Query
from src.DatabaseConnections.repositories.ms_repository import MsSqlServerRepository


class OperationsRepository(MsSqlServerRepository):
    model = "Skany"

    def get_by_id(self, entity_id: int) -> List[Tuple[Any]]:
        query: Query = f"""
            SELECT * FROM {self.model} WHERE indeks = {entity_id}
        """

        result: List[Tuple[Any]] = self.execute_query(query)

        return result

    def get_operation_detail(self, operation_id: int) -> List[Tuple[Any]]:
        query: Query = """
            SELECT
                sk.indeks AS id,
                sk.data AS startTime,
                z.zlecenie AS orderId,
                z.typ AS type,
                st.raport AS operationName,
                st.indeks AS workplaceID,
                u.imie AS firstName,
                u.nazwisko AS lastName
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
                JOIN Uzytkownicy u ON sk.uzytkownik = u.indeks
            WHERE sk.indeks = ?
        """
        params: Tuple[Any] = operation_id

        result: List[Tuple[Any]] = self.execute_query(query, params)

        return result

    def get_next_operation(
        self, operation_id: int, startTime: datetime, workplaceID: int
    ) -> List[Tuple[Any]]:
        query: Query = """
            SELECT TOP 1
                sk.data AS endTime
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
                JOIN Stanowiska st ON sk.stanowisko = st.indeks
            WHERE sk.indeks > ? AND sk.data > ? AND st.indeks = ?
            ORDER BY sk.data
        """
        params: Tuple[Any] = (operation_id, startTime, workplaceID)

        result: List[Tuple[Any]] = self.execute_query(query, params)

        return result

    def get_operation_control_data(self, stanowisko: int) -> List[Tuple[Any]]:
        query: Query = """
            SELECT
                MAX(Skany.indeks),
                Zlecenia.Zlecenie,
                Zlecenia.DataWejscia
            FROM Skany
            JOIN Skany_vs_Zlecenia ON Skany.indeks = Skany_vs_Zlecenia.IndeksSkanu
            JOIN Zlecenia ON Skany_vs_Zlecenia.IndeksZlecenia = Zlecenia.Indeks
            WHERE Skany.stanowisko = ?
            GROUP BY Zlecenia.Zlecenie, Zlecenia.DataWejscia
        """
        params: Tuple[Any] = (stanowisko,)

        result: List[Tuple[Any]] = self.execute_query(query, params)

        result = {
            "skany_index": result[0][0],
            "zlecenie": result[0][1],
            "execution_date": result[0][2],
        }

        return result

    def get_operations(
        self, operation_id: int, from_date: datetime, to_date: datetime
    ) -> List[Tuple[Any]]:
        query: Query = """
            SELECT
                sk.indeks AS id,
                sk.data AS startTime,
                LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime,
                z.zlecenie AS orderId
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
            WHERE sk.stanowisko = ? AND sk.data >= ? AND sk.data <= ?
            ORDER BY sk.data
        """
        params = (operation_id, from_date, to_date)

        result: List[Tuple[Any]] = self.execute_query(query, params)

        return result

    def get_all_operations(self) -> List[Tuple[Any]]:
        query: Query = """
            SELECT
                sk.indeks AS id,
                sk.stanowisko AS workplace,
                sk.data AS startTime,
                LEAD(sk.data) OVER (PARTITION BY sk.stanowisko ORDER BY sk.data) AS endTime
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
        """

        result: List[Tuple[Any]] = self.execute_query(query)

        return result