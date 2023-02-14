from django.db import models


class Actions(models.Model):
    camera = models.CharField(null=False, blank=False, max_length=50, default="now ip")
    start_tracking = models.DateTimeField(null=False, blank=False, max_length=50, default=None)
    stop_tracking = models.DateTimeField(null=False, blank=False, max_length=50, default=None)

    def __str__(self):
        return f"{self.camera}"

    class Meta:
        verbose_name = "IdleAction"
        verbose_name_plural = "IdleActions"


class Photos(models.Model):
    image = models.CharField(null=False, blank=False, max_length=250)
    idle_id = models.ForeignKey(Actions, on_delete=models.CASCADE, blank=False, null=False, related_name='photos')

    def __str__(self):
        return f"{self.idle_id}"

    class Meta:
        verbose_name = "PhotoAction"
        verbose_name_plural = "PhotoActions"
