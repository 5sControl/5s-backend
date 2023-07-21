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
            create_camera_algorithms,
            stop_and_update_algorithm,
        )

        camera_data, algorithm_data = self._get_algorithm_camera_data(camera_id)

        camera_algo_obj = CameraAlgorithm.objects.filter(
            camera_id=camera_id, algorithm__name="min_max_control"
        )

        if camera_algo_obj.exists():
            process_id = camera_algo_obj.first().process_id
            stop_and_update_algorithm(process_id)

        self.start(camera_data, algorithm_data)

        return

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

    def start(self, camera: Dict[str, str], algorithm: List[Dict[str, Any]]):
        from src.CameraAlgorithms.services.cameraalgorithm import camera_rtsp_link, send_run_request, save_data
        camera_obj: Camera = Camera.objects.get(id=camera["ip"])
        algorithm_obj: Algorithm = Algorithm.objects.get(name=algorithm["name"])
        rtsp_link: str = camera_rtsp_link(camera_obj.id)

        data: List[Dict[str, Any]] = []
        areas: List[Dict[str, Any]] = []
        stelag: List[Dict[str, Any]] = []

        zones: List[Optional[Dict[str, int]]] = algorithm.get("config", {}).get(
            "zonesID", []
        )

        request: Dict[str, Any] = {
            "camera_url": rtsp_link,
            "algorithm": algorithm_obj.name,
            "server_url": SERVER_URL,
            "extra": data,
        }

        algorithm_items: Iterable[Items] = Items.objects.filter(camera=camera_obj.id)

        for item in algorithm_items:
            areas.append(
                {
                    "itemId": item.id,
                    "itemName": item.name,
                    "coords": item.coords,
                    "lowStockLevel": item.low_stock_level,
                    "task": item.object_type,
                }
            )

        for zone_id in zones:
            zone_camera = ZoneCameras.objects.get(id=zone_id["id"], camera=camera_obj)

            stelag.append(
                {
                    "zoneId": zone_camera.id,
                    "zoneName": zone_camera.name,
                    "coords": zone_camera.coords,
                }
            )

        new_data: Dict[str, Any] = {
            "areas": areas,
            "zones": stelag,
        }
        data.append(new_data)
        request["extra"] = data

        response: Dict[str, Any] = send_run_request(request)
        save_data(
            algorithm_obj=algorithm_obj,
            camera_obj=camera_obj,
            pid=response["pid"],
            zones=zones,
        )
