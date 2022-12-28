from django.db import models
from apps.Locations.models import Location
from django.contrib.auth.models import AbstractUser


class ImageUsers(models.Model):
    image_user = models.ImageField(upload_to='Image')


class CustomUser(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    dataset = models.TextField(verbose_name='Date Set user', blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ManyToManyField(ImageUsers)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'


class History(models.Model):
    people = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='people_in_location', default='not known')
    location = models.ForeignKey(Location, related_name='Location_users',
                                 on_delete=models.CASCADE, blank=True, null=True)
    entry_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(default=None)
    image = models.ImageField(verbose_name='Image', blank=True, null=True, upload_to='images')

    def __str__(self):
        return f'{self.people}'

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Stories'
