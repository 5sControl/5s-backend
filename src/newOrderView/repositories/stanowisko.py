from typing import Any, List, Tuple

from src.Core.types import Query
from src.DatabaseConnections.repositories.ms_repository import WinHRepository


class WorkplaceRepository(WinHRepository):
    def get_workplaces_names(self) -> List[str]:
        query: Query = """
                SELECT DISTINCT Raport
                FROM Stanowiska
            """

        list_of_names: List[str] = []

        result: List[Tuple[Any]] = self.execute_query(query)

        for operation_names in result:
            list_of_names.append(operation_names[0])

        return list_of_names

    def get_raports(self, operation_type_ids: List[int] = None) -> List[Tuple[Any]]:
        query: Query = """
            SELECT
                indeks AS id,
                raport AS operationName
            FROM Stanowiska
            WHERE 1=1
        """

        if operation_type_ids:
            query += " AND indeks IN ({})" "".format(
                ",".join(str(id) for id in operation_type_ids)
            )

        result: List[Tuple[Any]] = self.execute_query(query)

        return result
