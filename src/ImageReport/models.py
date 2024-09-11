from django.db import models

from src.Reports.models import Report


class Image(models.Model):
    image = models.CharField(null=False, blank=False, max_length=250)
    date = models.CharField(null=False, blank=False, max_length=250)
    report_id = models.ForeignKey(
        Report,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="photos",
    )

    def __str__(self):
        return f"{self.report_id}"

    class Meta:
        verbose_name = "ImageReport"
        verbose_name_plural = "ImageReports"
        db_table = "images_reports"
