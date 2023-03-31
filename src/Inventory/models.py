from django.db import models

from src.Cameras.models import Camera
from src.Reports.models import Report
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm
from src.Algorithms.models import CameraAlgorithm

from django.db.models import Q

from src.Algorithms.utils import yolo_proccesing


class Items(models.Model):
    """Models items"""

    name = models.TextField(max_length=75, verbose_name="Item name")
    status = models.CharField(max_length=20, default="Out of stock")
    current_stock_level = models.IntegerField(verbose_name="Current stock level", default=0)
    low_stock_level = models.IntegerField(verbose_name="Low stock level")
    email = models.EmailField(blank=True, null=True, verbose_name="Email to send notifications")
    camera = models.ForeignKey(Camera, related_name='camera_id', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    coords = models.JSONField(verbose_name="Area coordinates", blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_update = bool(self.pk)
        instance = super().save(*args, **kwargs)
        if is_update:
            # stopped process
            from src.Algorithms.service import algorithms_services
            process_id = CameraAlgorithm.objects.filter(
                Q(camera_id=self.camera) & Q(algorithm__name='min_max_control')
            ).values_list('process_id', flat=True).first()
            if process_id is not None:
                yolo_proccesing.stop_process(pid=process_id)
                algorithms_services.update_status_of_algorithm_by_pid(pid=process_id)

            # started process
            camera = Camera.objects.filter(id=self.camera)
            algorithm = Algorithm.objects.filter(name='min_max_control')
            algorithms_services.create_new_records(cameras=[camera], algorithm=algorithm)

        return instance
