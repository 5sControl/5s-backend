from django.db import models


class Actions(models.Model):
    camera = models.CharField(null=True, blank=True, max_length=50)
    start_tracking = models.CharField(null=True, blank=True, max_length=50)
    stop_tracking = models.CharField(null=True, blank=True, max_length=50)


class Photos(models.Model):
    photo = models.ImageField(upload_to='Photo action')
    idle_id = models.ForeignKey(Actions, on_delete=models.CASCADE, blank=True, null=True)
