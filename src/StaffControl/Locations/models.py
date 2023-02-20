from django.db import models
from src.Cameras.models import Camera


class Gate(models.Model):
    name = models.CharField(max_length=30)
    camera_input = models.ForeignKey(
        Camera, related_name="DeviceInput", on_delete=models.CASCADE
    )
    camera_output = models.ForeignKey(
        Camera, related_name="DeviceOutput", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=30)
    gate_id = models.ForeignKey(Gate, related_name="Gate", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
