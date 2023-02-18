from django.db import models


class OperationsCounter(models.Model):
    date_time = models.CharField(max_length=50, blank=False, null=False, verbose_name="datetime_operations")
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.date_time}"

    class Meta:
        verbose_name = "Counter"
        verbose_name_plural = "Counters"
