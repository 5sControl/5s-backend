from celery import shared_task

import logging

from src.Core.utils import Sender
from src.CameraAlgorithms.models.algorithm import Algorithm

logger = logging.getLogger(__name__)


@shared_task
def uploading_algorithm(id_algorithm, image_name):
    """Background loading of the algorithm"""

    algorithm = Algorithm.objects.get(id=id_algorithm)
    result = Sender("loading", image_name)
    if result.status:
        algorithm.date_created = result.get("date")
        algorithm.save()
        return "success True"
    else:
        return logger.warning(f"Error loading {algorithm.image_name}")
