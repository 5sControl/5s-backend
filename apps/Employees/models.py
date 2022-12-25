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
    location = models.ForeignKey(Location, related_name='users', on_delete=models.CASCADE, blank=True, null=True)
    people = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='people_in_location', default='not known')
    entry_data = models.DateTimeField(auto_now_add=True)
    release_data = models.DateTimeField(blank=True, null=True)
    dataset_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(verbose_name='Image', blank=True, null=True)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Stories'
