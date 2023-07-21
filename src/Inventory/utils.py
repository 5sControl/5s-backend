import logging
from typing import Any, Dict, List, Tuple, Iterable, Optional

from src.CameraAlgorithms.models.algorithm import CameraAlgorithm, Algorithm
from src.CameraAlgorithms.models.camera import Camera, ZoneCameras
from src.Core.const import SERVER_URL
from src.Inventory.models import Items

logger = logging.getLogger(__name__)


class HandleItemUtils:
    def save_new_items(self, camera_id: int) -> None:
        from src.CameraAlgorithms.services.cameraalgorithm import (
            create_single_camera_algorithms,
            stop_and_update_algorithm,
        )

        camera_data, algorithm_data = self._get_algorithm_camera_data(camera_id)

        camera_algo_obj = CameraAlgorithm.objects.filter(
            camera_id=camera_id, algorithm__name="min_max_control"
        )

        if camera_algo_obj.exists():
            process_id = camera_algo_obj.first().process_id
            stop_and_update_algorithm(process_id)

        create_single_camera_algorithms(camera_data, algorithm_data)

    def delete_items(self, camera_id, items_count):
        from src.CameraAlgorithms.services.cameraalgorithm import (
            create_camera_algorithms,
            stop_and_update_algorithm,
        )

        camera_data, algorithm_data = self._get_algorithm_camera_data(camera_id)

        camera_algo_query = CameraAlgorithm.objects.filter(
            camera=camera_id, algorithm=8
        )

        if camera_algo_query.exists():
            stop_and_update_algorithm(camera_algo_query.first().process_id)

            if items_count > 0:
                create_camera_algorithms(camera_data, algorithm_data)

    def _get_algorithm_camera_data(
        self,
        camera_id: int,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        camera_obj: Camera = Camera.objects.get(id=camera_id)

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

        config: Dict[str, List[Any]] = {"zonesID": camera_algo_zones_prev}
        algorithm_data: Dict[str, Any] = {
            "name": "min_max_control",
            "config": config,
        }

        return camera_data, algorithm_data
