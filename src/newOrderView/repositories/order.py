from typing import Any, List, Tuple

from src.Core.types import Query
from src.DatabaseConnections.repositories.ms_repository import WinHRepository

from datetime import datetime


class OrderRepository(WinHRepository):
    def get_orders_by_operation(
        self, from_date: str, to_date: str, operation_type_ids: List[int]
    ) -> List[Tuple[Any]]:
        query: Query = """
            SELECT
                sk.indeks AS id,
                z.zlecenie AS orderId,
                sk.data AS startTime,
                LEAD(sk.data) OVER (ORDER BY sk.data) AS endTime
            FROM Skany sk
                JOIN Skany_vs_Zlecenia sz ON sk.indeks = sz.indeksskanu
                JOIN zlecenia z ON sz.indekszlecenia = z.indeks
            WHERE sk.data >= ? AND sk.data <= ?
        """

        params: Tuple[Any] = (from_date, to_date)

        if operation_type_ids:
            query += " AND sk.stanowisko IN ({})" "".format(
                ",".join(str(id) for id in operation_type_ids)
            )

        result: List[Tuple[Any]] = self.execute_query(query, params)

        return result

    def packing_time_search(self, order_number):
        query: Query = """
                SELECT S.Data
                FROM Skany S
                JOIN Skany_vs_Zlecenia SZ ON S.indeks = SZ.indeksskanu
                JOIN Zlecenia Z ON SZ.indekszlecenia = Z.Indeks
                WHERE Z.Zlecenie = %s
                    AND S.Stanowisko = 43;
        """
        # query: Query = """
        #         SELECT Data
        #         FROM Zlecenia
        #         WHERE Zlecenie = %s AND Stanowisko = 43;
        #     """
        params: Tuple[Any] = (order_number,)

        result: List[Tuple[Any]] = self.execute_query(query, params)

        result_in_milliseconds = [self.convert_to_milliseconds(row[0]) for row in result]

        return result_in_milliseconds

    def convert_to_milliseconds(self, timestamp):
        return int(datetime.timestamp(timestamp) * 1000)
