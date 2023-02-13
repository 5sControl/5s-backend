from django.db import models


class Idles(models.Model):
    camera = models.TextField(null=True, blank=True, max_length=50, related_name='ip cameras')
    start_tracking = models.TextField(null=True, blank=True, max_length=50, related_name='date time start tracking')
    stop_tracking = models.TextField(null=True, blank=True, max_length=50, related_name='date time stop tracking')


class Photos(models.Model):
    photo = models.ImageField(upload_to='Photo action')
    idle_id = models.ForeignKey(Idles, on_delete=models.CASCADE, blank=True, null=True)
