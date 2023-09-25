from celery import shared_task

import logging

from src.Core.utils import Sender


logger = logging.getLogger(__name__)


@shared_task
def uploading_algorithm(algorithm):
    """Background loading of the algorithm"""

    result = Sender("loading", algorithm.image_name)
    if result.status:
        algorithm.date_created = result.get("date")
        algorithm.save()
        return "success True"
    else:
        return logger.warning(f"Error loading {algorithm.image_name}")
