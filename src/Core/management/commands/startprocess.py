from django.core.management.base import BaseCommand

from src.Inventory.models import Items
from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.utils import yolo_proccesing


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.start_process()

    def start_process(self) -> None:
        all_camera_algorithms = CameraAlgorithm.objects.filter(is_active=True).exclude(
            process_id=None
        )
        for camera_algorithm in all_camera_algorithms:
            data = []
            if camera_algorithm.algorithm.name == "min_max_control":
                algorithm_items = Items.objects.filter(camera=camera_algorithm.camera)
                for item in algorithm_items:
                    data.append(
                        {
                            "itemId": item.id,
                            "coords": item.coords,
                            "itemName": item.name,
                        }
                    )
            try:
                result = yolo_proccesing.start_yolo_processing(
                    camera=camera_algorithm.camera,
                    algorithm=camera_algorithm.algorithm,
                    data=data,
                )
            except Exception:
                continue
            else:
                new_process_id = result["pid"]

                camera_algorithm.process_id = new_process_id
                camera_algorithm.save()
