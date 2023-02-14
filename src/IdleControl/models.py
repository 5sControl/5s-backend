from django.db import models


class Actions(models.Model):
    camera = models.CharField(null=True, blank=True, max_length=50)
    start_tracking = models.CharField(null=True, blank=True, max_length=50)
    stop_tracking = models.CharField(null=True, blank=True, max_length=50)

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
