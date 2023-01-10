from tabnanny import verbose

from django.db import models
from apps.Locations.models import Location, Camera

import face_recognition


class CustomUser(models.Model):
    first_name = models.CharField(default='Unknown', max_length=40, blank=True, null=True)
    last_name = models.CharField(default='Unknown', max_length=40, blank=True, null=True)
    dataset = models.TextField(verbose_name='Date Set user', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    status = models.BooleanField(default=False, verbose_name='Status in location',)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'


class History(models.Model):
    people = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='people_in_location')
    location = models.ForeignKey(Location, related_name='Location_users',
                                 on_delete=models.CASCADE, blank=True, null=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(blank=True, null=True)
    image = models.CharField(verbose_name='Image', blank=True, null=True, max_length=200)
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE, verbose_name='NameCamera')
    action = models.CharField(verbose_name='action camera', blank=True, null=True, max_length=50)


    def __str__(self):
        return f'{self.location}'

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'
