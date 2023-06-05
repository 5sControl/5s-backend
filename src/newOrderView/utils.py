from datetime import datetime


def add_ms(time: str) -> datetime:
    if "." not in time:
        time += ".000000"
    result: datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

    return result
