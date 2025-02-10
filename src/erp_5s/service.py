import base64
import json
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models import Prefetch, Q
from django.http import HttpResponse

from src.CameraAlgorithms.models import ZoneCameras
from src.OrderView.utils import get_skany_video_info, get_playlist_camera
from src.erp_5s.models import Orders, OrderItems, OrderOperations, OrderOperationTimespan, ReferenceItems
from src.erp_5s.models import Operations
from src.newOrderView.models import FiltrationOperationsTypeID
from src.erp_5s.serializers import ReferenceItemsSerializer, OrderOperationsSerializer


def get_operations():
    result = []
    operations = Operations.objects.all()
    for operation in operations:
        result.append(
            {
                "id": operation.id,
                "operationName": operation.name
            }
        )
    return result


def get_workplace_data():
    items = ReferenceItems.objects.filter(reference__name="workplace")
    serializer = ReferenceItemsSerializer(items, many=True)
    return serializer.data


def get_orders_with_details(from_date_obj, to_date_obj):
    selected_operations = Operations.objects.filter(
        id__in=FiltrationOperationsTypeID.objects.filter(type_erp="5s_control")
        .values_list('operation_type_id', flat=True)
    )

    filtered_operations = Prefetch(
        'orderoperations_set',
        queryset=OrderOperations.objects.filter(operation__in=selected_operations)
        .select_related('operation')
        .prefetch_related(
            Prefetch(
                'orderoperationtimespan_set',
                queryset=OrderOperationTimespan.objects.filter(
                    Q(started_at__lte=to_date_obj, finished_at__gte=from_date_obj) |
                    Q(started_at__gte=from_date_obj, started_at__lte=to_date_obj) |
                    Q(finished_at__gte=from_date_obj, finished_at__lte=to_date_obj)
                ).select_related('employee')
            )
        )
    )

    filtered_items = Prefetch(
        'orderitems_set',
        queryset=OrderItems.objects.prefetch_related(filtered_operations)
    )

    orders = Orders.objects.prefetch_related(filtered_items)

    result = []
    for order in orders:
        order_data = {
            'id': order.id,
            'order_number': order.order_number,
            'name': order.name,
            'status': order.status,
            'order_items': []
        }
        for item in order.orderitems_set.all():
            item_data = {
                'id': item.id,
                'name': item.name,
                'quantity': item.quantity,
                'operations': []
            }
            for operation in item.orderoperations_set.all():
                operation_data = {
                    'id': operation.id,
                    'operation_id': operation.operation.id,
                    'operation_name': operation.operation.name,
                    'timespans': []
                }
                for timespan in operation.orderoperationtimespan_set.all():
                    timespan_data = {
                        'id': timespan.id,
                        'started_at': timespan.started_at,
                        'finished_at': timespan.finished_at,
                        'employee': {
                            'id': timespan.employee.id,
                            'username': timespan.employee.username
                        } if timespan.employee else None
                    }
                    operation_data['timespans'].append(timespan_data)
                item_data['operations'].append(operation_data)
            order_data['order_items'].append(item_data)
        result.append(order_data)

    return result


def edit_response_for_orders_view(data, type_operation):
    result = []
    all_operations = set()

    if type_operation == 'orders':

        for order in data:
            duration = 0
            duration_expected = 0
            order_id = order.get("order_number")
            order_items = order.get("order_items", [])

            for item in order_items:
                operations = item.get("operations", [])

                for operation in operations:
                    timespans = operation.get("timespans")
                    if not timespans:
                        continue
                    for timespan in timespans:
                        started_at = timespan.get("started_at")
                        finished_at = timespan.get("finished_at")

                        if started_at and finished_at:
                            if isinstance(started_at, str):
                                started_at_dt = datetime.strptime(started_at, "%d.%m.%Y %H:%M:%S")
                            else:
                                started_at_dt = started_at

                            if isinstance(finished_at, str):
                                finished_at_dt = datetime.strptime(finished_at, "%d.%m.%Y %H:%M:%S")
                            else:
                                finished_at_dt = finished_at

                            delta = finished_at_dt - started_at_dt
                            duration += delta.total_seconds()
            if duration != 0:
                result.append(
                    {
                        "orId": order_id,
                        "duration": duration * 1000,
                        "duration_expected": duration_expected * 1000
                    }
                )
        return result

    else:
        operations = FiltrationOperationsTypeID.objects.filter(type_erp="5s_control")

        for item in operations:
            all_operations.add((item.name, item.operation_type_id))

        for workplace_name, operation_id in all_operations:
            oprs = []

            for ordered_dict in data:
                id_value = ordered_dict.get('order_number')
                orders_items = ordered_dict.get('order_items')
                if orders_items:
                    for item in orders_items:
                        operations = item.get("operations", [])
                        for operation in operations:
                            timespans = operation.get("timespans")
                            if not timespans:
                                continue
                            for timespan in timespans:
                                if operation.get("operation_id") == operation_id:
                                    started_at = timespan.get("started_at")
                                    finished_at = timespan.get("finished_at")
                                    if isinstance(started_at, str):
                                        started_at_dt = datetime.strptime(started_at, "%d.%m.%Y %H:%M:%S")
                                    else:
                                        started_at_dt = started_at

                                    if isinstance(finished_at, str):
                                        finished_at_dt = datetime.strptime(finished_at, "%d.%m.%Y %H:%M:%S")
                                    else:
                                        finished_at_dt = finished_at

                                    if started_at_dt and finished_at_dt:
                                        started_at_ts = started_at_dt.timestamp() * 1000
                                        finished_at_ts = finished_at_dt.timestamp() * 1000
                                        oprs.append({
                                            "id": timespan.get("id"),
                                            "orId": str(id_value),
                                            "sTime": started_at_ts,
                                            "eTime": finished_at_ts
                                        })

            result.append({
                "oprTypeID": operation_id,
                "oprName": workplace_name,
                "oprs": oprs
            })

        sorted_result = sorted(result, key=lambda x: x["oprTypeID"], reverse=True)
        return sorted_result


def get_reports_orders_view(from_date, to_date, type_operation):
    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
    to_date_obj = to_date_obj.replace(hour=23, minute=59, second=59)

    data = get_orders_with_details(from_date_obj, to_date_obj)
    result = edit_response_for_orders_view(data, type_operation)
    return result


def get_detail_information_by_operation(operation_id):
    videos = []

    timestamp = OrderOperationTimespan.objects.get(id=operation_id)
    # workplace_id = timestamp.employee.workplace_id
    workplace_id = timestamp.workplace_number
    order_id = timestamp.order_operation.order_id
    order = Orders.objects.get(id=order_id)

    sTime = int(timestamp.started_at.timestamp() * 1000) if timestamp.started_at else None
    eTime = int(timestamp.finished_at.timestamp() * 1000) if timestamp.finished_at else None

    cameras_zones = ZoneCameras.objects.filter(index_workplace=workplace_id)

    if workplace_id:
        for zone_camera in cameras_zones:
            camera_id = zone_camera.camera.id
            video = get_skany_video_info(sTime, camera_id)
            get_playlist_camera(sTime, eTime, camera_id)

            if video not in videos:
                if not eTime:
                    eTime = int(datetime.now().timestamp() * 1000)
                playlist_content = get_playlist_camera(sTime, eTime, camera_id)
                video['playlist'] = base64.b64encode(playlist_content).decode('utf-8')
                videos.append(video)

    if not timestamp.employee:
        username = timestamp.employee.username
    else:
        username = None
    result = {
        "id": timestamp.id,
        "orId": order.id,
        "oprName": order.name,
        # "url": url,
        # "elType": elementType,
        "sTime": sTime,
        "eTime": eTime,
        "frsName": username,
        # "lstName": lastName,
        "status": order.status,
        "videos": videos,
    }
    return result

