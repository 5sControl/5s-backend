from django.core.management.base import BaseCommand

from ....core.logger import logger

from src.Algorithms.models import CameraAlgorithm
from src.Algorithms.utils import yolo_proccesing


class Command(BaseCommand):
    """
    Checks if any processes have been started and
    puts them back to work at the start of the project
    """

    def handle(self, *args, **options):
        self.start_process()
        logger.info("Processes started successfully")

    def start_process(self):
        all_camera_algorithms = CameraAlgorithm.objects.filter(is_active=True).exclude(
            process_id=None
        )
        print(all_camera_algorithms)
        # result = yolo_proccesing.start_yolo_processing(...)
        print(all_camera_algorithms)
