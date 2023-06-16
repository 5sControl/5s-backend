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


def convert_to_gmt0(input_time: datetime) -> datetime:
    gmt0 = pytz.timezone("Etc/GMT")
    if input_time.tzinfo != gmt0:
        dt_gmt_plus3 = input_time.astimezone(gmt0)
        return dt_gmt_plus3
    else:
        return input_time


def convert_to_unix(input_time: datetime) -> int:
    return int(input_time.timestamp()) * 1000
