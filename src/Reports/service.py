from typing import List, Dict
from datetime import datetime, timezone
import logging

from src.CameraAlgorithms.models import Camera
from src.MsSqlConnector.services import create_records

from src.Reports.models import Report, SkanyReport
from src.OrderView.models import IndexOperations

logger = logging.getLogger(__name__)


def edit_extra(data: List[Dict], camera: Camera):
    operation_index = (
        IndexOperations.objects.filter(camera=camera.id)
        .values("type_operation")
        .last()["type_operation"]
    )
    extra_data = create_records.operation_control_data(operation_index)

    if len(data) >= 1:
        data[0]["skany_index"] = int(extra_data["skany_index"])
        data[0]["zlecenie"] = str(extra_data["zlecenie"])
        data[0]["execution_date"] = str(extra_data["execution_date"])
    else:
        data.append(
            {
                "skany_index": int(extra_data["skany_index"]),
                "zlecenie": str(extra_data["zlecenie"]),
                "execution_date": str(extra_data["execution_date"]),
            }
        )

    logger.warning(f"final operation data is -> {data}")
    return data


def create_skanyreport(
    report: Report,
    report_data: List[Dict],
    violation_found: bool,
    start_tracking: str,
    end_tracking: str
) -> None:
    start_dt = datetime.strptime(start_tracking, "%Y-%m-%d %H:%M:%S.%f")
    start_utc = start_dt.replace(tzinfo=timezone.utc)
    sTime = int(start_utc.timestamp())

    end_dt = datetime.strptime(end_tracking, "%Y-%m-%d %H:%M:%S.%f")
    end_utc = end_dt.replace(tzinfo=timezone.utc)
    eTime = int(end_utc.timestamp())

    skany_indeks = report_data[0].get("skany_index")
    zlecenie = report_data[0].get("zlecenie")
    execution_date = report_data[0].get("execution_date")

    logger.warning(f"Creating Skany Report start_tracking -> {start_tracking} - {sTime}, end_tracking -> {end_tracking} - {eTime}")

    SkanyReport.objects.create(
        report=report,
        skany_index=skany_indeks,
        zlecenie=zlecenie,
        execution_date=execution_date,
        violation_found=violation_found,
        start_time=sTime,
        end_time=eTime,
    )