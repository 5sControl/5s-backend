from django.db import models


class Action(models.Model):
    camera = models.CharField(null=True, blank=True, max_length=50)
    photo_start = models.ImageField(upload_to='Photo start detekt', blank=True, null=True)
    photo_stop = models.ImageField(upload_to='Photo stop detekt', blank=True, null=True)
    start_tracking = models.CharField(null=True, blank=True, max_length=50)
    stop_tracking = models.CharField(null=True, blank=True, max_length=50)

