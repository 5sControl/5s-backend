from django.db import models


class Actions(models.Model):
    camera = models.CharField(null=True, blank=True, max_length=50)
    start_tracking = models.CharField(null=True, blank=True, max_length=50)
    stop_tracking = models.CharField(null=True, blank=True, max_length=50)


class Photos(models.Model):
    image = models.CharField(null=False, blank=False, max_length=250)
    idle_id = models.ForeignKey(Actions, on_delete=models.CASCADE, blank=False, null=False)
