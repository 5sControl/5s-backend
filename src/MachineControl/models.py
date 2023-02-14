from django.db import models


class MachineAction(models.Model):
    camera = models.CharField(null=False, blank=False, max_length=50, default="now ip")
    photo_start = models.CharField(blank=False, null=False, max_length=250, default="now photo")
    photo_stop = models.CharField(blank=False, null=False, max_length=250, default="now photo")
    start_tracking = models.DateTimeField(null=False, blank=False, max_length=50, default=None)
    stop_tracking = models.DateTimeField(null=False, blank=False, max_length=50, default=None)

    def __str__(self):
        return f"{self.camera}"

    class Meta:
        verbose_name = "MachineAction"
        verbose_name_plural = "MachineActions"
