from django.db import models
from apps.Locations.models import Location
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    location = models.ForeignKey(Location, related_name='Location_users', on_delete=models.CASCADE, blank=True, null=True)
    dataset = models.TextField(verbose_name='Date Set user', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'


class History(models.Model):
    people = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='people_in_location', default='not known')
    entry_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(default=None)
    image = models.ImageField(verbose_name='Image', blank=True, null=True, upload_to='images')

    def __str__(self):
        return f'{self.people}'

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Stories'
