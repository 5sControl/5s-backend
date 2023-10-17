from celery import shared_task

from dateutil.parser import parse

import logging

from src.CameraAlgorithms.services.cameraalgorithm import stop_and_update_algorithm, create_camera_algorithms
from src.Core.utils import Sender
from src.CameraAlgorithms.models.algorithm import Algorithm, CameraAlgorithm, Camera

logger = logging.getLogger(__name__)


@shared_task
def uploading_algorithm(id_algorithm, image_name):
    """Background loading of the algorithm"""

    algorithm = Algorithm.objects.get(id=id_algorithm)
    result = Sender("loading", image_name)
    if result.get("status"):
        date_created = parse(result.get("date"))
        print("date_created", date_created)
        algorithm.date_created = date_created
        algorithm.download_status = True
        algorithm.save()
        logger.info(f"loading is complete is {algorithm.image_name}")
        restart_loading_algorithm(id_algorithm, algorithm.name)
        return "success True"
    else:
        return logger.warning(f"Error loading {algorithm.image_name}")


def restart_loading_algorithm(algorithm_id, algorithm_name):
    camera_algorithms = CameraAlgorithm.objects.filter(algorithm_id=algorithm_id)
    for algorithm in camera_algorithms:
        camera = Camera.objects.get(id=algorithm.camera_id)
        zones = algorithm.zones
        algorithms = [{"algorithms": [{"name": algorithm_name, "config": {"zonesID": [zones]}}]}]

        # stopping processing
        stop_and_update_algorithm(algorithm.process_id)

        # start processing
        create_camera_algorithms(camera, algorithms)
