import logging
from typing import Dict, Any

from django.core.management.base import BaseCommand

from src.Core.const import DJANGO_SERVICE_URL
from src.Core.exceptions import SenderError, InvalidResponseError
from src.Inventory.models import Items

from src.CameraAlgorithms.models.camera import ZoneCameras
from src.CameraAlgorithms.models import Camera, CameraAlgorithm, Algorithm
from src.CameraAlgorithms.services.cameraalgorithm import (
    camera_rtsp_link,
    send_run_request,
)

logger = logging.getLogger(__name__)


# class Command(BaseCommand):
#     def handle(self, *args, **kwargs):
#         self.start_process()

def start_process() -> None:
    camera_algorithms = CameraAlgorithm.objects.filter(is_active=True).exclude(
        process_id=None
    )

    for camera_algorithm in camera_algorithms:
        extra_params = []
        camera_obj: Camera = camera_algorithm.camera
        algorithm_obj: CameraAlgorithm = camera_algorithm.algorithm
        rtsp_link: str = camera_rtsp_link(camera_obj.id)

        request: Dict[str, Any] = {
            "camera_url": rtsp_link,
            "algorithm": algorithm_obj.name,
            "image_name": algorithm_obj.image_name,
            "server_url": DJANGO_SERVICE_URL,
            "link_reports": f"{DJANGO_SERVICE_URL}:8000/api/reports/report-with-photos/",
            "extra": extra_params,
        }

        all_zones = camera_algorithm.zones
        all_cords = []
        for zone_id in all_zones:
            zone_camera = ZoneCameras.objects.get(
                id=zone_id["id"], camera=camera_obj
            )
            coords = zone_camera.coords
            coords[0]["zoneId"] = zone_camera.id
            coords[0]["zoneName"] = zone_camera.name

            all_cords.append(coords[0])

        request["extra"] = [{"coords": all_cords}]

        if camera_algorithm.algorithm.name == "min_max_control":
            algorithm_items = Items.objects.filter(camera=camera_obj)
            areas = []
            zones = []

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

            all_zones = camera_algorithm.zones
            try:
                for zone_id in all_zones:
                    zone_camera = ZoneCameras.objects.get(
                        id=zone_id["id"], camera=camera_obj
                    )

                    zones.append(
                        {
                            "zoneId": zone_camera.id,
                            "zoneName": zone_camera.name,
                            "coords": zone_camera.coords,
                        }
                    )
            except Exception as e:
                logger.critical(f"Error while collecting zone: {e}")

            new_data = {"areas": areas, "zones": zones}
            extra_params.append(new_data)
            request["extra"] = extra_params

        try:
            result = send_run_request(request)
            logger.info(
                f"Algorithm successfully started. Request {request}, Result {result}"
            )
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
