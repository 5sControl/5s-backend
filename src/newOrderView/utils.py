from datetime import datetime
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


def convert_to_timezone(input_time: datetime, timezone: str) -> datetime:
    target_timezone = pytz.timezone(timezone)
    if input_time.tzinfo != target_timezone:
        converted_time = input_time.astimezone(target_timezone)
        return converted_time
    else:
        return input_time


def convert_to_unix(input_time: datetime) -> int:
    return int(input_time.timestamp()) * 1000
