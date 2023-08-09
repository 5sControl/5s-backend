from typing import Any, List, Tuple
import logging

from django.core.management.base import BaseCommand

from src.newOrderView.models import FiltrationOperationsTypeID
from src.newOrderView.repositories.stanowisko import WorkplaceRepository

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **options):
        logger.info("Starting fill stanowisko")
        self.fill_stanowisko()

    def fill_stanowisko(self):
        workplace_repo: WorkplaceRepository = WorkplaceRepository()
        stanowiska_data: List[Tuple[Any]] = workplace_repo.get_raports()

        for id in stanowiska_data:
            oprtID = id[0]
            oprtName = id[1]
            if not FiltrationOperationsTypeID.objects.filter(
                operation_type_id=oprtID
            ).exists():
                FiltrationOperationsTypeID.objects.create(
                    operation_type_id=oprtID, name=oprtName
                )
