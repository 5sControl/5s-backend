from django.db import models


class MachineAction(models.Model):
    camera = models.CharField(null=True, blank=True, max_length=50)
    photo_start = models.CharField(blank=True, null=True, max_length=250)
    photo_stop = models.CharField(blank=True, null=True, max_length=250)
    start_tracking = models.DateTimeField(null=True, blank=True, max_length=50)
    stop_tracking = models.DateTimeField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"{self.camera}"

    class Meta:
        verbose_name = "MachineAction"
        verbose_name_plural = "MachineActions"
