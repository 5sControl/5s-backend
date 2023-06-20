from datetime import datetime, timedelta
import hashlib


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
