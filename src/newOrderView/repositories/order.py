from typing import Any, List, Tuple

from src.Core.types import Query
from src.DatabaseConnections.repositories.ms_repository import MsSqlServerRepository


class OrderRepository(MsSqlServerRepository):
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
            query += " AND st.indeks IN ({})" "".format(
                ",".join(str(id) for id in operation_type_ids)
            )

        result: List[Tuple[Any]] = self.execute_query(query, params)

        return result
