from django.db import models

from src.Cameras.models import Camera
from src.Reports.models import Report


class StatusItemChoice(models.TextChoices):
    in_stock = 'In stock'
    low_stock_level = 'Low stock level'
    out_of_stock = 'Out of stock'


class Items(models.Model):
    """Models items"""

    name = models.TextField(max_length=75, verbose_name="Item name")
    status = models.CharField(max_length=20, choices=StatusItemChoice.choices, default=StatusItemChoice.out_of_stock)
    current_stock_level = models.IntegerField(verbose_name="Current stock level", blank=True, null=True)
    low_stock_level = models.IntegerField(verbose_name="Low stock level")
    email = models.EmailField(blank=True, null=True, verbose_name="Email to send notifications")
    camera = models.ForeignKey(Camera, related_name='camera_id', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Date created", auto_now=True)

    def __str__(self):
        return self.name
