from django.db import models

from src.StaffControl.Locations.models import Camera


class Algorithm(models.Model):
    """
    The Algorithm model represents a single algorithm
    """

    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)


class CameraAlgorithm(models.Model):
    """
    The CameraAlgorithm model represents a camera that uses a specific algorithm
    """

    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    camera_id = models.ForeignKey(Camera, on_delete=models.CASCADE)
