import logging
from typing import Dict, Any

from django.core.management.base import BaseCommand

from src.Core.const import SERVER_URL
from src.Core.exceptions import SenderError, InvalidResponseError
from src.Inventory.models import Items

from src.CameraAlgorithms.models.camera import ZoneCameras
from src.CameraAlgorithms.models import Camera, CameraAlgorithm
from src.CameraAlgorithms.services.cameraalgorithm import (
    camera_rtsp_link,
    send_run_request,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.start_process()

    def start_process(self) -> None:
        camera_algorithms = CameraAlgorithm.objects.filter(is_active=True).exclude(
            process_id=None
        )

        for camera_algorithm in camera_algorithms:
            extra_params = []
            camera_obj: Camera = camera_algorithm.camera
            algorithm_obj: CameraAlgorithm = camera_algorithm.algorithm
            rtsp_link: str = camera_rtsp_link(camera_obj.id)

            if camera_algorithm.algorithm.name == "min_max_control":
                algorithm_items = Items.objects.filter(camera=camera_obj)
                print("algorithm_items", algorithm_items)
                areas = []
                stelag = []

                for item in algorithm_items:
                    areas.append(
                        {"itemId": item.id, "itemName": item.name, "coords": item.coords}
                    )

                all_zones = camera_obj.zones

                for zone_id in all_zones:
                    zone_camera = ZoneCameras.objects.get(id=zone_id["id"], camera=camera_obj)

                    stelag.append(
                        {"zoneId": zone_camera.id, "zoneName": zone_camera.name, "coords": zone_camera.coords}
                    )

                new_data = {
                    "areas": areas,
                    "zones": stelag
                }
                print("New data", new_data)
                extra_params.append(new_data)

            request: Dict[str, Any] = {
                "camera_url": rtsp_link,
                "algorithm": algorithm_obj.name,
                "server_url": SERVER_URL,
                "extra": extra_params,
            }
            print("request", request)

            try:
                result = send_run_request(request)
            except SenderError as e:
                logger.critical(f"Yolo server is not available. Details: {e}")
            except InvalidResponseError as e:
                logger.critical(
                    f"Yolo can't start algorithm {algorithm_obj.name} on camera {camera_obj.id}. Details: {e}"
                )
            else:
                new_process_id = result["pid"]

                camera_algorithm.process_id = new_process_id
                camera_algorithm.save()
