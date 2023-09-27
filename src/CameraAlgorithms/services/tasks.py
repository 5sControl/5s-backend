from celery import shared_task

from datetime import datetime, timezone

import logging

from src.Core.utils import Sender
from src.CameraAlgorithms.models.algorithm import Algorithm

logger = logging.getLogger(__name__)


@shared_task
def uploading_algorithm(id_algorithm, image_name):
    """Background loading of the algorithm"""

    algorithm = Algorithm.objects.get(id=id_algorithm)
    result = Sender("loading", image_name)
    if result.get("status"):
        date_str = result.get("date")
        date_created = datetime.fromisoformat(date_str.replace('Z', '+00:00')).astimezone(timezone.utc)

        algorithm.date_created = date_created
        algorithm.download_status = True
        algorithm.save()
        return "success True"
    else:
        return logger.warning(f"Error loading {algorithm.image_name}")
