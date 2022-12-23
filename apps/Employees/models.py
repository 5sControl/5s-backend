from django.db import models
from apps.Locations.models import Location
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    location = models.ForeignKey(Location, related_name='Location_users', on_delete=models.CASCADE, blank=True, null=True)
    data_set = models.TextField(verbose_name='Date Set user', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'


