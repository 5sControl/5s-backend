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


def edit_response_for_orders_by_5s(data, type_operation):
    result = []
    all_operations = set()

    if type_operation == 'orders':

        for orders in data:
            duration = 0
            duration_expected = 0
            for order in orders.get("extra"):
                duration_zones = order.get("duration_zones")
                if duration_zones:
                    for zone in duration_zones:
                        order_duration = zone.get("all_durations") or 0.0
                        order_duration_expected = zone.get("duration_expected") or 0.0

                        duration += (order_duration * 60)
                        duration_expected += (order_duration_expected * 60)

                    result.append(
                        {
                            "orId": orders.get('id'),
                            "duration": duration * 1000,
                            "duration_expected": duration_expected * 1000
                        }
                    )
        return result

    else:
        connection = ConnectionInfo.objects.filter(used_in_orders_view=True).first()
        operations = FiltrationOperationsTypeID.objects.filter(type_erp=connection.erp_system)

        for item in operations:
            all_operations.add((item.name, item.operation_type_id))

        for workplace_name, operation_id in all_operations:
            oprs = []

            for ordered_dict in data:
                id_value = ordered_dict.get('id')
                extra_value = ordered_dict.get('extra')
                if extra_value:
                    for report in extra_value:
                        duration_zones = report.get("duration_zones")
                        if duration_zones:
                            for zone in duration_zones:
                                if zone.get("zone_id") == operation_id:
                                    try:
                                        start_time = int(datetime.strptime(zone.get('start_time'),
                                                                           "%Y-%m-%d %H:%M:%S.%f").timestamp() * 1000)
                                        end_time = start_time + (zone.get('all_durations') * 1000)

                                        oprs.append({
                                            "id": operation_id,
                                            "orId": str(id_value),
                                            "sTime": start_time,
                                            "eTime": end_time
                                        })
                                    except ValueError as e:
                                        print(f"Time conversion error: {e}")

            result.append({
                "oprTypeID": operation_id,
                "oprName": workplace_name,
                "oprs": oprs
            })

        sorted_result = sorted(result, key=lambda x: x["oprTypeID"], reverse=True)
        return sorted_result


def get_reports_orders_5s(from_date, to_date, type_operation):

    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
    to_date_obj = to_date_obj.replace(hour=23, minute=59, second=59)

    queryset = Report.objects.filter(
        Q(date_created__gte=from_date_obj),
        Q(date_created__lte=to_date_obj),
        Q(extra__contains=[{'duration_zones': []}])
    ).order_by("-date_created", "-id")
    serializer = ReportSerializersForOrders5s(queryset, many=True)
    result = edit_response_for_orders_by_5s(serializer.data, type_operation)
    return result
