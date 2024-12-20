import logging

from django.db import models
from django.contrib.postgres.fields import ArrayField

from src.CameraAlgorithms.models import Camera
from src.CompanyLicense.models import Company
from src.Inventory.utils import HandleItemUtils

logger = logging.getLogger(__name__)


class Items(models.Model):
    OBJECT_TYPE_CHOICES = [
        ("bottle", "Bottle"),
        ("box", "Box"),
        ("red line", "Red Line"),
    ]

    name = models.TextField(max_length=75, verbose_name="Item name")
    object_type = models.CharField(
        max_length=20,
        choices=OBJECT_TYPE_CHOICES,
        verbose_name="Object type",
    )
    status = models.CharField(max_length=20, default="Out of stock")
    current_stock_level = models.IntegerField(
        verbose_name="Current stock level", default=0
    )
    low_stock_level = models.IntegerField(verbose_name="Low stock level", default=0)
    camera = models.ForeignKey(
        Camera, related_name="camera_id", on_delete=models.SET_NULL, null=True
    )
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    coords = models.JSONField(verbose_name="Area coordinates")
    prev_status = models.TextField(
        verbose_name="Previous status",
        default=None,
        max_length=30,
        blank=True,
        null=True,
    )
    suppliers = models.ForeignKey(
        Company,
        related_name="Supplier",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    order_quantity = models.IntegerField(
        verbose_name="Order quantity", blank=True, null=True
    )
    to_emails = ArrayField(
        models.EmailField(), verbose_name="To_emails", blank=True, null=True
    )
    copy_emails = ArrayField(
        models.EmailField(), verbose_name="Copy_emails", blank=True, null=True
    )
    subject = models.CharField(
        verbose_name="Subject message", max_length=60, blank=True, null=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        utils = HandleItemUtils()
        is_update = bool(self.pk)
        camera_updated = (
            self.pk
            and self.camera_id != self.__class__.objects.get(pk=self.pk).camera_id
        )
        coords_updated = (
            self.pk and self.coords != self.__class__.objects.get(pk=self.pk).coords
        )

        if self.coords:
            from src.Inventory.service import is_valid_coordinates
            self.coords = is_valid_coordinates(self.coords, "item")

        instance = super().save(*args, **kwargs)

        if not is_update or camera_updated or coords_updated:
            logger.warning(f"Restarting CameraAlgorithm with new items")
            utils.save_new_items(self.camera_id)

        return instance

    def delete(self, *args, **kwargs):
        utils = HandleItemUtils()
        instance = super().delete(*args, **kwargs)
        items_count = len(Items.objects.filter(camera_id=self.camera_id))
        utils.delete_items(self.camera_id, items_count)

        logger.warning(f"Deleted MinMaxControl")
        return instance
