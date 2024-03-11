import logging
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class HandleItemUtils:
    def save_new_items(self, camera_id) -> None:
        from src.CameraAlgorithms.services.cameraalgorithm import (
            create_single_camera_algorithms,
            stop_and_update_algorithm,
        )
        from src.CameraAlgorithms.models import CameraAlgorithm, Algorithm

        all_algorithms_id = Algorithm.objects.filter(used_in="inventory")

        for used_algorithm_id in all_algorithms_id:
            algorithm_id = used_algorithm_id.id
            camera_data, algorithm_data = self._get_algorithm_camera_data_min_max(camera_id)

            camera_algo_obj = CameraAlgorithm.objects.filter(
                camera_id=camera_id, algorithm__id=algorithm_id
            )

            if camera_algo_obj:
                process_id = camera_algo_obj.first().process_id
                if process_id:
                    stop_and_update_algorithm(process_id)

            create_single_camera_algorithms(camera_data, algorithm_data)

    def delete_items(self, camera_id, items_count):
        from src.CameraAlgorithms.services.cameraalgorithm import (
            create_single_camera_algorithms,
            stop_and_update_algorithm,
        )
        from src.CameraAlgorithms.models import CameraAlgorithm

        all_camera_algo_query = CameraAlgorithm.objects.filter(algorithm__used_in="inventory")

        for camera_algo_query in all_camera_algo_query:
            camera_data, algorithm_data = self._get_algorithm_camera_data_min_max(camera_algo_query.camera_id)

            if camera_algo_query:
                stop_and_update_algorithm(camera_algo_query.process_id)

                if items_count > 0:
                    create_single_camera_algorithms(camera_data, algorithm_data)

    def save_new_zone(self, zone_id: int) -> None:
        from src.CameraAlgorithms.services.cameraalgorithm import (
            create_single_camera_algorithms,
            stop_and_update_algorithm,
        )
        from src.CameraAlgorithms.models import CameraAlgorithm, Camera

        camera_algorithms: List[CameraAlgorithm] = self.get_camera_algorithms_by_zone_id(zone_id)
        logger.warning(f"With zone {zone_id} was found {camera_algorithms}")

        for camera_algorithm_obj in camera_algorithms:
            camera_obj: Camera = Camera.objects.get(id=camera_algorithm_obj.camera.pk)
            zone: List[Dict[str, int]] = camera_algorithm_obj.zones
            process_id: int = camera_algorithm_obj.process_id
            camera_data: Dict[str, str] = {
                "ip": camera_obj.pk,
                "name": camera_obj.name,
                "username": camera_obj.username,
                "password": camera_obj.password,
            }

            config: Dict[str, List[Any]] = {"zonesID": zone}
            algorithm_data: Dict[str, Any] = {
                "name": camera_algorithm_obj.algorithm.name,
                "config": config,
            }
            logger.warning("Stopping process")
            stop_and_update_algorithm(process_id)
            logger.warning("Starting process")
            create_single_camera_algorithms(camera_data, algorithm_data)

    def get_camera_algorithms_by_zone_id(self, zone_id: int):
        from src.CameraAlgorithms.models import CameraAlgorithm
        return CameraAlgorithm.objects.filter(zones__contains=[{"id": zone_id}])

    def _get_algorithm_camera_data_min_max(
        self,
        camera_id: int,
    ) -> Tuple[Dict[str, str], Dict[str, Any]]:
        from src.CameraAlgorithms.models import CameraAlgorithm, Camera

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
