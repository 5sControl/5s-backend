from django.db import models
from django.core.validators import RegexValidator


class Camera(models.Model):
    """Model for saving camera information"""

    id = models.CharField(
        primary_key=True,
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                message="ID must be a valid IP address",
            )
        ],
    )
    name = models.CharField(max_length=100, blank=True, null=True)

    username = models.CharField(max_length=100, default="admin", blank=True, null=True)
    password = models.CharField(max_length=250, default="admin", blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.id
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"


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
