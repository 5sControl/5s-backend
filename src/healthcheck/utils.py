import psutil


def get_cpu_load_percentage():
    return psutil.cpu_percent(interval=5)


def get_healthckeck_data():
    return {
        'cpu_load': get_cpu_load_percentage()
    }
