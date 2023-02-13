from django.db import models


class Action(models.Model):
    camera = models.TextField(null=True, blank=True, max_length=50, related_name='ip cameras')
    photo_start = models.ImageField(upload_to='Photo start detekt', blank=True, null=True)
    photo_stop = models.ImageField(upload_to='Photo stop detekt', blank=True, null=True)
    start_tracking = models.TextField(null=True, blank=True, max_length=50, related_name='date time start tracking')
    stop_tracking = models.TextField(null=True, blank=True, max_length=50, related_name='date time stop tracking')

