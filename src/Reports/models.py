from django.db import models

from src.CameraAlgorithms.models import Algorithm
from src.CameraAlgorithms.models import Camera


class StatusReportChoice(models.TextChoices):
    false = "false"
    true = "true"


class Report(models.Model):
    """Model report"""

    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)
    camera = models.ForeignKey(Camera, null=True, on_delete=models.SET_NULL)
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
        db_table = "report"


class SkanyReport(models.Model):
    """
    Models skany report 'id'
    """
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    skany_index = models.IntegerField(null=True, verbose_name="skany index")
    zlecenie = models.CharField(max_length=50, blank=True, null=True)
    violation_found = models.BooleanField(blank=True, null=True)
    execution_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        verbose_name = "ReportSkany"
        verbose_name_plural = "ReportsSkany"
        db_table = "skany_report"
