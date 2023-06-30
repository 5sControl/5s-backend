from typing import Any, List, Tuple
import logging

import pyodbc

from django.core.management.base import BaseCommand

from src.Core.types import Query
from src.DatabaseConnections.services import connector as connector_service
from src.newOrderView.models import FiltrationOperationsTypeID

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Starting fill stanowisko")
        self.fill_stanowisko()

    def fill_stanowisko(self):
        connection: pyodbc.Connection = connector_service.get_database_connection()

        stanowiska_query: Query = """
            SELECT
                st.indeks AS id,
                st.raport AS operationName
            FROM Stanowiska st
        """

        stanowiska_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=stanowiska_query
        )

        for id in stanowiska_data:
            oprtID = id[0]
            oprtName = id[1]
            if not FiltrationOperationsTypeID.objects.filter(operation_type_id=oprtID).exists():
                FiltrationOperationsTypeID.objects.create(operation_type_id=oprtID, name=oprtName)
