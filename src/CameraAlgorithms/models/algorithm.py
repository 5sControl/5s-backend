from datetime import datetime

from django.db import models
from django.http import HttpResponse

from src.CameraAlgorithms.models import Camera

from src.Core.utils import Sender


class Algorithm(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image_name = models.CharField(max_length=150, blank=True, null=True, unique=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(blank=True, null=True)
    is_available = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    download_status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Algorithm"
        verbose_name_plural = "Algorithms"

        db_table = "algorithm"

    def save(self, *args, **kwargs):

        if self.is_available:
            result = Sender("search", self.image_name)
            if result.get('status'):
                if result.get("download"):
                    self.download_status = True
                    date_string = result.get("date")
                    date_string = date_string.split(".")[0]
                    date_obj = datetime.fromisoformat(date_string)
                    self.date_created = date_obj
                    super().save(*args, **kwargs)
                    return HttpResponse("Image loaded successfully", status=200)
                else:
                    self.download_status = False
                    super().save(*args, **kwargs)
                    return HttpResponse("Image not loaded", status=200)
            else:
                raise ValueError(f" Error, {self.image_name} there is no such name")


class CameraAlgorithm(models.Model):
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    process_id = models.PositiveBigIntegerField(default=0)
    zones = models.JSONField(blank=True, null=True, verbose_name="Id zones algorithm")

    def __str__(self):
        return f"{self.algorithm} - {self.camera}"

    class Meta:
        verbose_name = "CameraAlgorithm"
        verbose_name_plural = "CameraAlgorithms"

        db_table = "cameraalgorithm"


class CameraAlgorithmLog(models.Model):
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

    class Meta:
        verbose_name = "CameraAlgorithmLog"
        verbose_name_plural = "CameraAlgorithmLogs"

        db_table = "cameraalgorithmslog"
