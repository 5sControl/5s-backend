from django.db import models

from src.Cameras.models import Camera


class Algorithm(models.Model):
    """
    The Algorithm model represents a single algorithm
    """

    name = models.CharField(max_length=100)
    is_available = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class CameraAlgorithm(models.Model):
    """
    The CameraAlgorithm model represents a camera that uses a specific algorithm
    """

    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    process_id = models.PositiveIntegerField(blank=True, null=True)
    yolo_url = models.CharField(max_length=200, blank=False, null=False)


class CameraAlgorithmLog(models.Model):
    """
    Contains information about a deleted and created camera algorithm
    """

    algorithm_name = models.CharField(max_length=150)
    camera_ip = models.CharField(max_length=150)
    stoped_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.created_at and self.stoped_at:
            if self.created_at > self.stoped_at:
                self.status = True
            else:
                self.status = False
        super(CameraAlgorithmLog, self).save(*args, **kwargs)
