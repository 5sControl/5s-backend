from typing import List, Dict

from src.Cameras.models import Camera
from src.MsSqlConnector.services import create_records

from src.Reports.models import Report, SkanyReport
from src.OrderView.models import IndexOperations


def edit_extra(data: List[Dict], camera: Camera):
    operation_index = IndexOperations.objects.filter(camera=camera.id).values('type_operation').last()[
        'type_operation']
    extra_data = create_records.extra_data(operation_index)

    if len(data) >= 1:
        data[0]["skany_index"] = int(extra_data["skany_index"])
        data[0]["zlecenia_index"] = int(extra_data["zlecenia_index"])
        data[0]["execution_date"] = str(extra_data["execution_date"])
    else:
        data.append({
            "skany_index": int(extra_data["skany_index"]),
            "zlecenia_index": int(extra_data["zlecenia_index"]),
            "execution_date": str(extra_data["execution_date"]),
        })

    print("data is ", data)
    return data


def create_skanyreport(report: Report, report_data: Dict, violation_found: bool):
    """
    Save skany index and report in database
    """

    skany_indeks = report_data.get("skany_index")
    zlecenia_index = report_data.get("zlecenia_index")
    execution_date = report_data.get("execution_date")

    SkanyReport.objects.create(
        report=report,
        skany_index=skany_indeks,
        zlecenia_index=zlecenia_index,
        execution_date=execution_date,
        violation_found=violation_found
    )
