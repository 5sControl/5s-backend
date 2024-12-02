from datetime import datetime

from django.db.models import Prefetch, Q

from src.CameraAlgorithms.models import ZoneCameras
from src.OrderView.utils import get_skany_video_info
from src.erp_5s.models import Orders, OrderItems, OrderOperations, OrderOperationTimespan, ReferenceItems
from src.erp_5s.models import Operations
from src.newOrderView.models import FiltrationOperationsTypeID
from src.erp_5s.serializers import OrdersSerializer, OrderOperationsSerializer, OperationsSerializer


def get_workplace_data():
    items = ReferenceItems.objects.filter(reference__name="workplace")
    serializer = OperationsSerializer(items, many=True)
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
                    Q(started_at__range=(from_date_obj, to_date_obj)) |
                    Q(finished_at__range=(from_date_obj, to_date_obj))
                ).select_related('employee')
            )
        )
    )

    filtered_items = Prefetch(
        'orderitems_set',
        queryset=OrderItems.objects.prefetch_related(filtered_operations)
    )

    orders = Orders.objects.prefetch_related(filtered_items)

    serializer = OrdersSerializer(orders, many=True)
    return serializer.data


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
                            started_at_dt = datetime.strptime(started_at, "%d.%m.%Y %H:%M:%S")
                            finished_at_dt = datetime.strptime(finished_at, "%d.%m.%Y %H:%M:%S")

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
                                if operation.get("operation").get("id") == operation_id:
                                    started_at = timespan.get("started_at")
                                    finished_at = timespan.get("finished_at")
                                    if started_at and finished_at:

                                        started_at_dt = datetime.strptime(started_at,
                                                                          "%d.%m.%Y %H:%M:%S").timestamp() * 1000
                                        finished_at_dt = datetime.strptime(finished_at,
                                                                           "%d.%m.%Y %H:%M:%S").timestamp() * 1000
                                        oprs.append({
                                            "id": timespan.get("id"),
                                            "orId": str(id_value),
                                            "sTime": started_at_dt,
                                            "eTime": finished_at_dt
                                        })

            result.append({
                "oprTypeID": operation_id,
                "oprName": workplace_name,
                "oprs": oprs
            })

        sorted_result = sorted(result, key=lambda x: x["oprTypeID"], reverse=True)
        return sorted_result
        # return data


def get_reports_orders_view(from_date, to_date, type_operation):
    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d")
    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d")
    to_date_obj = to_date_obj.replace(hour=23, minute=59, second=59)

    data = get_orders_with_details(from_date_obj, to_date_obj)
    result = edit_response_for_orders_view(data, type_operation)
    return result


def get_detail_information_by_operation(operation_id):
    timestamp = OrderOperationTimespan.objects.get(id=operation_id)
    order_operation = timestamp.order_operation
    order_item = order_operation.order_item

    order = order_item.order

    order_serializer = OrdersSerializer(order)
    order_operation_serializer = OrderOperationsSerializer(order_operation)

    camera_zone = ZoneCameras.objects.get(index_workplace=order_operation.operation.id)
    camera_id = camera_zone.camera.id

    sTime = int(timestamp.started_at.timestamp() * 1000) if timestamp.started_at else None
    eTime = int(timestamp.finished_at.timestamp() * 1000) if timestamp.finished_at else None

    result = {
        "id": timestamp.id,
        "orId": order.id,
        "oprName": order.name,
        # "url": url,
        # "elType": elementType,
        "sTime": sTime,
        "eTime": eTime,
        "frsName": timestamp.employee.username,
        # "lstName": lastName,
        "status": order.status,
        "video": get_skany_video_info(sTime, camera_id),
    }
    return result
