from typing import Any, List, Dict
from datetime import datetime, timedelta
import logging

from src.CameraAlgorithms.models import Camera
from src.DatabaseConnections.models import ConnectionInfo

from src.Reports.models import Report, SkanyReport
from src.OrderView.models import IndexOperations
from src.Reports.serializers import ReportSerializersForOrders5s
from src.newOrderView.models import FiltrationOperationsTypeID
from src.newOrderView.repositories.operations import OperationsRepository
from django.db.models import Q

logger = logging.getLogger(__name__)


def edit_extra(extra: Dict[str, Any], camera: Camera):
    try:
        operation_repo: OperationsRepository = OperationsRepository()

        operation_index = (
            IndexOperations.objects.filter(camera=camera.id)
            .values("type_operation")
            .last()["type_operation"]
        )

        extra_data = operation_repo.get_operation_control_data(operation_index)

        extra["skany_index"] = int(extra_data["skany_index"])
        extra["zlecenie"] = str(extra_data["zlecenie"])
        extra["execution_date"] = str(extra_data["execution_date"])
    except Exception as index_error:
        print(f"IndexError occurred: {index_error}")
    print("Field extra operation_control", extra)
    return extra


def create_skanyreport(
    report: Report,
    report_data: List[Dict],
    violation_found: bool,
    start_tracking: str,
    end_tracking: str,
) -> None:
    start_dt = datetime.strptime(start_tracking, "%Y-%m-%d %H:%M:%S.%f")
    sTime = int(start_dt.timestamp())

    end_dt = datetime.strptime(end_tracking, "%Y-%m-%d %H:%M:%S.%f")
    eTime = int(end_dt.timestamp())

    skany_indeks = report_data.get("skany_index")
    zlecenie = report_data.get("zlecenie")
    execution_date = report_data.get("execution_date")

    logger.warning(
        f"Creating Skany Report start_tracking -> {start_tracking} - {sTime}, end_tracking -> {end_tracking} - {eTime}"
    )

    SkanyReport.objects.create(
        report=report,
        skany_index=skany_indeks,
        zlecenie=zlecenie,
        execution_date=execution_date,
        violation_found=violation_found,
        start_time=sTime,
        end_time=eTime,
    )
