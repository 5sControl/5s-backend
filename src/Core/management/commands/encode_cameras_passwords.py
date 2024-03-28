from django.core.management.base import BaseCommand
from src.CameraAlgorithms.models import Camera
from src.CameraAlgorithms.services.security import is_encrypted

import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Encode passwords for all cameras'

    def handle(self, *args, **options):
        cameras = Camera.objects.all()
        for camera in cameras:
            if not is_encrypted(camera.password):
                camera.save()
                print(f"Camera {camera.id} encrypted password")
                logger.info(f"Camera {camera.id} encrypted password")
            else:
                print(f"Camera {camera.id} password is already encrypted")
                logger.info(f"Camera {camera.id} password is already encrypted")
        self.stdout.write(self.style.SUCCESS('Successfully encoded passwords for all cameras'))
