from collections import defaultdict
from typing import Iterable, List, Any, Optional, Tuple, Dict
from datetime import datetime, timedelta, time
import logging

from django.db.models import Q
from django.contrib.postgres.fields import JSONField
from django.db.models.query import QuerySet

from src.CameraAlgorithms.models.camera import Camera, ZoneCameras
from src.OrderView.models import IndexOperations
from src.OrderView.utils import get_skany_video_info
from src.Reports.models import Report, SkanyReport
from src.newOrderView.repositories.stanowisko import WorkplaceRepository

from ..repositories import OperationsRepository
from ..utils import add_ms, calculate_duration, convert_to_gmt0, convert_to_unix

logger = logging.getLogger(__name__)


class OperationServices:
    @staticmethod
    def get_operations(
        from_date: str, to_date: str, operation_type_ids: List[int]
    ) -> List[Dict[str, Any]]:
        workplace_repo: WorkplaceRepository = WorkplaceRepository()
        operation_repo: OperationsRepository = OperationsRepository()

        stanowiska_data: List[Tuple[Any]] = workplace_repo.get_raports(
            operation_type_ids
        )

        result_list: List[Dict[str, Any]] = []

        for row in stanowiska_data:
            operation_id: int = row[0]
            operation_name: str = row[1]


            from_date_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d") + timedelta(microseconds=1)
            to_date_dt: datetime = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)

            operations_data = operation_repo.get_operations(
                operation_id=operation_id, from_date=from_date_dt, to_date=to_date_dt
            )

            operations_list: List[Dict[str, Any]] = []

            if not operations_data:
                continue

            for i in range(len(operations_data)):
                operation_row: Tuple[Any] = operations_data[i]

                id: int = operation_row[0]
                orderId: str = operation_row[3].strip()
                startTime: str = str(
                    operation_row[1]
                )  # FIXME -> whithout transform datetime to str
                endTime: str = (
                    str(operation_row[2]) if i < len(operations_data) - 1 else None
                )

                operation: Dict[str, Any] = {
                    "id": id,
                    "orId": orderId,
                    "sTime": startTime,
                    "eTime": endTime,
                }

                startTime_dt: datetime = add_ms(startTime)
                startTime_dt: datetime = convert_to_gmt0(startTime_dt)
                startTime_unix: int = convert_to_unix(startTime_dt)
                operation["sTime"]: int = startTime_unix

                if endTime is not None:
                    endTime_dt: datetime = add_ms(endTime)
                    endTime_dt: datetime = convert_to_gmt0(endTime_dt)

                    if endTime_dt.date() > startTime_dt.date():
                        endTime_dt: datetime = startTime_dt + timedelta(hours=1)
                    else:
                        endTime_dt: datetime = endTime_dt or startTime_dt + timedelta(
                            hours=1
                        )

                    endTime_unix: int = convert_to_unix(endTime_dt)
                    operation["eTime"]: int = endTime_unix
                else:
                    endTime_dt = startTime_dt + timedelta(hours=1)
                    endTime_unix: int = convert_to_unix(endTime_dt)
                    operation["eTime"]: int = endTime_unix

                operations_list.append(operation)

            result = {
                "oprTypeID": operation_id,
                "oprName": operation_name,
                "oprs": operations_list,
            }

            result_list.append(result)
        return result_list

    @staticmethod
    def get_machine(
        from_date: str, to_date: str, operation_type_ids: List[int]
    ) -> List[Dict[str, Any]]:
        workplace_repo: WorkplaceRepository = WorkplaceRepository()

        stanowiska_data: List[Tuple[Any]] = workplace_repo.get_raports(
            operation_type_ids
        )

        result_list: List[Dict[str, Any]] = []

        for row in stanowiska_data:
            operation_id: int = row[0]

            zone_cameras_ids: Iterable[int] = ZoneCameras.objects.filter(
                index_workplace=operation_id
            ).values_list("id", flat=True)
            zone_cameras_ids: List[int] = [
                JSONField().to_python(id) for id in zone_cameras_ids
            ]

            if not zone_cameras_ids:
                continue

            from_date_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d")
            from_date_dt: datetime = from_date_dt + timedelta(microseconds=1)

            to_date_dt: datetime = datetime.strptime(to_date, "%Y-%m-%d")
            to_date_dt: datetime = (
                to_date_dt + timedelta(days=1) - timedelta(microseconds=1)
            )

            reports_with_matching_zona_id: Iterable[
                QuerySet[Report]
            ] = Report.objects.filter(Q(algorithm=3) & Q(extra__has_key="zoneId"))

            if not reports_with_matching_zona_id:
                continue

            for zone_camera_id in zone_cameras_ids:
                zone_reports: Iterable[
                    QuerySet[Report]
                ] = reports_with_matching_zona_id.filter(
                    Q(extra__zoneId__exact=zone_camera_id)
                    & Q(start_tracking__gte=from_date_dt)
                    & Q(stop_tracking__lte=to_date_dt)
                    & Q(start_tracking__lte=to_date)
                    & Q(stop_tracking__gte=from_date)
                )

                if not zone_reports:
                    continue

                filtered_reports: List[QuerySet] = [
                    report
                    for report in zone_reports
                    if time(6)
                    <= datetime.strptime(
                        report.start_tracking, "%Y-%m-%d %H:%M:%S.%f"
                    ).time()
                    <= time(20)
                    and time(6)
                    <= datetime.strptime(
                        report.stop_tracking, "%Y-%m-%d %H:%M:%S.%f"
                    ).time()
                    <= time(20)
                ]

                reports: List[Dict[str, Any]] = []
                zone_name: Optional[str] = None

                for report in filtered_reports:
                    zone_data: Dict[str, Any] = report.extra
                    camera_ip: str = report.camera.id

                    zone_name: str = zone_data["zoneName"]

                    machine_control_report_id: int = report.id

                    sTime: str = convert_to_unix(
                        datetime.strptime(report.start_tracking, "%Y-%m-%d %H:%M:%S.%f")
                    )
                    eTime: str = convert_to_unix(
                        datetime.strptime(report.stop_tracking, "%Y-%m-%d %H:%M:%S.%f")
                    )

                    report_data: Dict[str, Any] = {
                        "zoneId": machine_control_report_id,  # Machine control report from dashboard
                        "orId": zone_name,  # Zone name
                        "camera": camera_ip,
                        "sTime": sTime,
                        "eTime": eTime,
                    }

                    reports.append(report_data)

                machine_result: Dict[str, Any] = {
                    "oprTypeID": operation_id,  # Operation id (stanowisko)
                    "inverse": True,
                    "oprName": zone_name,  # Zone name
                    "oprs": reports,
                }
                result_list.append(machine_result)

        return result_list

    @staticmethod
    def get_whnet_operation() -> List[Dict[str, Any]]:
        workplace_repo: WorkplaceRepository = WorkplaceRepository()
        stanowiska_data: List[Tuple[Any]] = workplace_repo.get_raports()

        result_list: List[Dict[str, Any]] = []

        for order_row in stanowiska_data:
            order: Dict[str, Any] = {
                "id": int(order_row[0]),
                "operationName": str(order_row[1]).strip(),
            }

            result_list.append(order)

        return result_list

    @staticmethod
    def get_operation_by_details(operation_id: int) -> Dict[str, Any]:
        operation_repo: OperationsRepository = OperationsRepository()

        operation_data: List[Tuple[Any]] = operation_repo.get_operation_detail(
            operation_id
        )

        if operation_data:
            id: int = operation_data[0][0]
            startTime: datetime = operation_data[0][
                1
            ]  # FIXME -> whithout transform datetime to str
            orderId: str = str(operation_data[0][2]).strip()
            elementType: str = operation_data[0][3]
            operationName: str = operation_data[0][4]
            workplaceID: int = operation_data[0][5]
            firstName: str = operation_data[0][6]
            lastName: str = operation_data[0][7]

            video_data: Optional[Dict[str, Any]] = None

            endTime_query_result: List[Tuple[Any]] = operation_repo.get_next_operation(
                operation_id=operation_id, startTime=startTime, workplaceID=workplaceID
            )

            if endTime_query_result:
                endTime: Optional[str] = str(endTime_query_result[0][0])
            else:
                endTime: Optional[str] = None

            startTime_dt: datetime = add_ms(str(startTime))
            startTime_dt: datetime = convert_to_gmt0(startTime_dt)
            startTime_unix: int = convert_to_unix(startTime_dt)

            if endTime is not None:
                endTime_dt: datetime = add_ms(str(endTime))
                endTime_dt: datetime = convert_to_gmt0(endTime_dt)

                if endTime_dt.date() > startTime_dt.date():
                    endTime_dt: datetime = startTime_dt + timedelta(hours=1)
                else:
                    endTime_dt: datetime = endTime_dt or startTime_dt + timedelta(
                        hours=1
                    )

                endTime_unix: int = convert_to_unix(endTime_dt)
            else:
                endTime_dt = startTime_dt + timedelta(hours=1)
                endTime_unix: int = convert_to_unix(endTime_dt)

            camera_obj: Optional[Camera] = None
            operation_status: Optional[bool] = None
            video_data: Dict[str, bool] = {}

            skany_report: Optional[SkanyReport] = SkanyReport.objects.filter(
                skany_index=id
            ).first()
            camera_obj: Optional[Camera] = IndexOperations.objects.filter(
                type_operation=workplaceID
            ).first()

            if skany_report:
                operation_status: Optional[bool] = skany_report.violation_found
                video_time: Optional[bool] = skany_report.start_time

                if camera_obj and video_time:
                    video_data: Dict[str, Any] = get_skany_video_info(
                        time=(video_time), camera_ip=camera_obj.camera.id
                    )

            result: Dict[str, Any] = {
                "id": id,
                "orId": orderId,
                "oprName": operationName,
                "elType": elementType,
                "sTime": startTime_unix,
                "eTime": endTime_unix,
                "frsName": firstName,
                "lstName": lastName,
                "status": operation_status,
                "video": video_data,
            }

            return result
        else:
            return {}

    @staticmethod
    def culculate_avg_duration():
        operation_repo: OperationsRepository = OperationsRepository()

        operation_data: List[Tuple[Any]] = operation_repo.get_all_operations()

        workplace_duration_dict: Dict[str, Tuple[int, int]] = defaultdict(lambda: (0, 0))

        for operation_row in operation_data:
            workplace: str = operation_row[1].strip()
            start_time: datetime = operation_row[2]
            end_time: Optional[datetime] = operation_row[3]

            if end_time is not None:
                if end_time.date() > start_time.date():
                    end_time = start_time + timedelta(hours=1)
                else:
                    end_time = end_time or start_time + timedelta(hours=1)

            else:
                end_time = start_time + timedelta(hours=1)

            duration: int = calculate_duration(start_time, end_time)

            workplace_duration, workplace_count = workplace_duration_dict[workplace]
            workplace_duration += duration
            workplace_count += 1
            workplace_duration_dict[workplace] = (workplace_duration, workplace_count)

        result_list: List[Dict[str, Any]] = []

        for workplace, (workplace_duration, workplace_count) in workplace_duration_dict.items():
            average_duration = workplace_duration / workplace_count
            result_list.append({"workplace": workplace, "average_duration": average_duration})

        return result_list