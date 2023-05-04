from django.db import models

from src.Algorithms.models import Algorithm
from src.Cameras.models import Camera


class StatusReportChoice(models.TextChoices):
    false = "false"
    true = "true"


class Report(models.Model):
    """Model report"""

    algorithm = models.ForeignKey(Algorithm, on_delete=models.DO_NOTHING)
    camera = models.ForeignKey(Camera, on_delete=models.DO_NOTHING)
    start_tracking = models.CharField(max_length=100, blank=True, null=True)
    stop_tracking = models.CharField(max_length=100, blank=True, null=True)
    violation_found = models.BooleanField(blank=True, null=True, default=None)
    extra = models.JSONField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        choices=StatusReportChoice.choices, default="false", max_length=30
    )

    def __str__(self):
        return f"{self.algorithm}"

    class Meta:
        verbose_name = "Report"
        verbose_name_plural = "Reports"


class SkanyReport(models.Model):
    """
    Models skany report 'id'
    """
    report = models.ForeignKey(Report, on_delete=models.DO_NOTHING)
    skany_index = models.IntegerField(null=True, verbose_name="sany index")

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "ReportSkany"
        verbose_name_plural = "ReportsSkany"
