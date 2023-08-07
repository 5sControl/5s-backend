import logging

from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from src.Inventory.utils import HandleItemUtils

logger = logging.getLogger(__name__)


class Camera(models.Model):
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
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=250)

    name = models.CharField(max_length=100, blank=True, null=True)
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

        db_table = "camera"


class ZoneCameras(models.Model):
    camera = models.ForeignKey(
        Camera,
        on_delete=models.SET_NULL,
        related_name="Zone_cameras",
        blank=True,
        null=True,
    )
    coords = models.JSONField(verbose_name="Zone coordinates")
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    workplace = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="Workplace db Winkhaus"
    )
    index_workplace = models.IntegerField(
        default=None, null=True, blank=True, verbose_name="Index workplace Winkhaus"
    )
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)

    def __str__(self):
        return self.name

    def is_coordinate_positive(self, coord):
        return coord['x1'] > 0 and coord['x2'] > 0 and coord['y1'] > 0 and coord['y2'] > 0

    def calculate_area(self, coord):
        width = coord['x2'] - coord['x1']
        height = coord['y2'] - coord['y1']
        return width * height

    def remove_invalid_coordinates(self):
        valid_coords = []
        for coord in self.coords:
            if self.is_coordinate_positive(coord):
                area = self.calculate_area(coord)
                if area > 500:
                    valid_coords.append(coord)
        self.coords = valid_coords

    def save(self, *args, **kwargs):
        self.remove_invalid_coordinates()
        if len(self.coords) == 0:
            raise ValidationError("Unprocessable - Empty or negative data provided")

        utils = HandleItemUtils()
        is_update = bool(self.pk)
        coords_updated = (
            self.pk and self.coords != self.__class__.objects.get(pk=self.pk).coords
        )

        super().save(*args, **kwargs)

        if not is_update or coords_updated:
            logger.warning("Restarting CameraAlgorithm with new zone coors")
            utils.save_new_zone(self.camera_id)
