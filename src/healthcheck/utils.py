from typing import Dict, List, Any
import psutil

from src.CameraAlgorithms.models.camera import Camera


def get_cpu_load_percentage():
    return psutil.cpu_percent(interval=5)


def get_devices():
    camera: List[str] = Camera.objects.all().values_list("id")
    count: int = len(camera)
    return {
        "count": count,
        "devices": camera,
    }


def get_nvidia_gpu():
    return False


def get_healthckeck_data():
    cpu_load: float = get_cpu_load_percentage()
    devices: Dict[str, Any] = get_devices()
    nvidia_gpu: bool = get_nvidia_gpu()
    return {
        "cpu_load": cpu_load,
        "devices": devices,
        "nvidia_gpu": nvidia_gpu,
    }
