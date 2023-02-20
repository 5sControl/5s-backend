from django.db import models

from src.Algorithms.models import Algorithm
from src.Cameras.models import Camera


class Report(models.Model):
    """Model report"""
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    start_tracking = models.CharField(max_length=100, blank=True, null=True)
    stop_tracking = models.CharField(max_length=100, blank=True, null=True)
    violation_found = models.BooleanField(blank=True, null=True, default=None)
    extra = models.CharField(max_length=50, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.algorithm}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"
