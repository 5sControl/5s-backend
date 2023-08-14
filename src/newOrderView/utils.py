from datetime import datetime, timedelta
import hashlib
from typing import List, Tuple

from rest_framework.request import Request

from src.newOrderView.models import FiltrationOperationsTypeID


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
