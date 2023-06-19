from datetime import datetime, timedelta
import hashlib

import pytz


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
    gmt_plus3 = pytz.timezone("Etc/GMT+3")
    gmt0 = pytz.timezone("Etc/GMT")

    input_time = input_time.replace(tzinfo=gmt_plus3)

    converted_time = input_time.astimezone(gmt0) - timedelta(hours=3)
    return converted_time


def convert_to_unix(input_time: datetime) -> int:
    return int(input_time.timestamp()) * 1000
