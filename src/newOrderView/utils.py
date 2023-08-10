from datetime import datetime, timedelta
import hashlib
from typing import Any, Dict, List, Tuple

from django.shortcuts import get_object_or_404
from django.core.cache import cache

from rest_framework.request import Request

from src.DatabaseConnections.models import ConnectionInfo
from src.newOrderView.models import FiltrationOperationsTypeID
from src.newOrderView.services.connector import connector_services
from src.newOrderView.services.operations import OperationServices, OrderServices


def add_ms(time: str) -> datetime:
    if "." not in time:
        time += ".000000"
    result: datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

    return result


def generate_hash(prefix: str, from_date: str, to_date: str) -> str:
    data = prefix + ":" + from_date + ":" + to_date
    hash_object = hashlib.sha256(data.encode())
    return hash_object.hexdigest()


def convert_to_gmt0(input_time: datetime) -> datetime:
    return input_time - timedelta(hours=3)


def convert_to_unix(input_time: datetime) -> int:
    return int(input_time.timestamp()) * 1000


def calculate_duration(start_time: datetime, end_time: datetime) -> int:
    result = int((end_time - start_time).total_seconds() * 1000)
    return result


def get_cache_data(from_date: str, to_date: str) -> Tuple[str, List[int]]:
    operation_type_ids = FiltrationOperationsTypeID.objects.filter(
        is_active=True
    ).values_list("operation_type_id", flat=True)
    operation_type_ids = list(operation_type_ids)

    key: str = (
        generate_hash("get_order", from_date, to_date)
        + ":"
        + ":".join(str(id) for id in operation_type_ids)
    )

    return key, operation_type_ids


def get_date_interval(request: Request) -> Tuple[str]:
    from_date: str = request.GET.get("from")
    to_date: str = request.GET.get("to")

    return from_date, to_date


def get_response(cache_key: str, from_date: str, to_date: str, operation_type_ids: List[id], type: str) -> List[Dict[str, Any]]:
    connector = get_object_or_404(ConnectionInfo, is_active=True).type

    if connector == "api":
        print("API")
        if type == "operation":
            response: List[Dict[str, Any]] = connector_services.get_operations(from_date, to_date)
        elif type == "order":
            response: List[Dict[str, Any]] = OrderServices.get_order(from_date, to_date, operation_type_ids)
    elif connector == "database":
        response = cache.get(cache_key)
        if response is None:
            response: List[Dict[str, Any]] = OperationServices.get_operations(
                from_date, to_date, operation_type_ids
            )
            cache.set(cache_key, response, timeout=120)

    return response
