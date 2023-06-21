from typing import Any, List, Tuple
import logging

import pyodbc

from django.core.management.base import BaseCommand

from src.Core.types import Query
from src.MsSqlConnector.connector import connector as connector_service
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
                st.indeks AS id
            FROM Stanowiska st
        """

        stanowiska_data: List[Tuple[Any]] = connector_service.executer(
            connection=connection, query=stanowiska_query
        )

        for id in stanowiska_data:
            oprtID: int = id[0]
            if FiltrationOperationsTypeID.objects.exists(operation_type_id=oprtID):
                FiltrationOperationsTypeID.objects.create(operation_type_id=oprtID)
