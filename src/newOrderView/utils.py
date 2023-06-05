from datetime import datetime


def add_ms(time: str) -> datetime:
    if "." not in time:
        time += ".000000"
    result: datetime = datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")

    return result


def format_time(time_string: str) -> str:
    # Преобразование строки времени в объект datetime
    time_obj = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S.%f")
    # Форматирование времени в желаемый формат
    formatted_time = datetime.strftime(time_obj, "%Y-%m-%d %H:%M:%S.%f")
    return formatted_time
