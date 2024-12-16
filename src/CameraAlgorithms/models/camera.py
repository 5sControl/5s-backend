import logging

from django.db import models
from django.core.validators import RegexValidator

from src.Inventory.utils import HandleItemUtils
from src.CameraAlgorithms.services.security import encrypt

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
        if self._state.adding and self.password:
            self.password = encrypt(self.password)
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
        on_delete=models.CASCADE,
        related_name="Zone_cameras",
        blank=True,
        null=True,
    )
    coords = models.JSONField(verbose_name="Zone coordinates")
    name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    workplace = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Workplace in the system ERP"
    )
    index_workplace = models.IntegerField(
        default=None, null=True, blank=True, verbose_name="Index workplace"
    )
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    approximate_duration = models.IntegerField(
        verbose_name="Preliminary operation duration in seconds", default=5, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.coords:
            from src.Inventory.service import is_valid_coordinates
            self.coords = is_valid_coordinates(self.coords, "zone")

        utils = HandleItemUtils()
        is_update = bool(self.pk)
        coords_updated = (
            self.pk and self.coords != self.__class__.objects.get(pk=self.pk).coords
        )

        super().save(*args, **kwargs)

        if not is_update or coords_updated:
            logger.warning("Restarting CameraAlgorithm with new zone coors")
            utils.save_new_zone(self.pk)

    class Meta:
        verbose_name = "Camera zone"
        verbose_name_plural = "Camera zone"
        db_table = "camera_zones"
