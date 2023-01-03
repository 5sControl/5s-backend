from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image
from io import BytesIO

from apps.Locations.models import Location

import sys


class ImageUsers(models.Model):
    image_user = models.ImageField(upload_to='Image')


class CustomUser(models.Model):
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    dataset = models.TextField(verbose_name='Date Set user', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ManyToManyField(ImageUsers, blank=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'


class History(models.Model):
    people = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True,
                               related_name='people_in_location')
    location = models.ForeignKey(Location, related_name='Location_users',
                                 on_delete=models.CASCADE, blank=True, null=True)
    entry_date = models.DateTimeField(auto_now_add=True, blank=True)
    release_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(verbose_name='Image', blank=True, null=True, upload_to='images')

    def __str__(self):
        return f'{self.location}'

    def save(self, *args, **kwargs):
        # Opening the uploaded image
        im = Image.open(self.image)

        if im.mode == "JPEG":
            pass
        elif im.mode in ["RGBA", "P"]:
            im = im.convert("RGB")

        output = BytesIO()
        
        im.save(output, format='JPEG', subsampling=0, quality=95)
        output.seek(0)

        self.image = InMemoryUploadedFile(output, 'ImageField',
                                                  "%s.jpg" % self.image.name.split('.')[0], 'image/jpeg',
                                                  sys.getsizeof(output), None)
        super(History, self).save()


    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Stories'
