import logging
from typing import Any, Dict, List

from src.CameraAlgorithms.models.algorithm import CameraAlgorithm
from src.CameraAlgorithms.models.camera import Camera


logger = logging.getLogger(__name__)


def save_new_items(camera_id):
    from src.CameraAlgorithms.services.cameraalgorithm import create_camera_algorithms

    camera_data, algorithm_data = _get_algorithm_camera_data(camera_id)
    create_camera_algorithms(camera_data, algorithm_data)


def delete_items(camera_id, items_count):
    from src.CameraAlgorithms.services.cameraalgorithm import create_camera_algorithms, stop_and_update_algorithm

    camera_data, algorithm_data = _get_algorithm_camera_data(camera_id)

    camera_algo_query = CameraAlgorithm.objects.filter(camera=camera_id, algorithm=8)

    if camera_algo_query.exists():
        stop_and_update_algorithm(camera_algo_query.first().process_id)

        if items_count > 0:
            create_camera_algorithms(camera_data, algorithm_data)


def _get_algorithm_camera_data(camera_id: int):
    camera_obj: str = Camera.objects.get(id=camera_id)

    try:
        camera_algo_zones_prev: List[Dict[str, int]] = CameraAlgorithm.objects.get(
            algorithm=8, camera=camera_id
        ).zones
    except CameraAlgorithm.DoesNotExist:
        camera_algo_zones_prev = []

    camera_data: Dict[str, str] = {
        "ip": camera_id,
        "name": camera_obj.name,
        "username": camera_obj.username,
        "password": camera_obj.password,
    }

    config: Dict[str, Dict[str, List[Dict[str, int]]]] = {"zonesID": camera_algo_zones_prev}
    algorithm_data: List[Dict[str, Any]] = [
        {
            "name": "min_max_control",
            "config": config,
        }
    ]

    return camera_data, algorithm_data