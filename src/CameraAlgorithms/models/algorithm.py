from django.db import models

from src.CameraAlgorithms.models import Camera


class Algorithm(models.Model):
    name = models.CharField(max_length=100)
    image_name = models.CharField(max_length=150, blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Algorithm"
        verbose_name_plural = "Algorithms"

        db_table = "algorithm"


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
