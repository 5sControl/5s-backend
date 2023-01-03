from django.db import models
from apps.Locations.models import Location
from django.contrib.auth.models import AbstractUser
import os
import face_recognition
from PIL import Image, ImageDraw
import pickle
import cv2


class ImageUsers(models.Model):
    image_user = models.ImageField(upload_to='attachments')


class CustomUser(models.Model):
    first_name = models.CharField(max_length=40, blank=True, null=True)
    last_name = models.CharField(max_length=40, blank=True, null=True)
    dataset = models.TextField(verbose_name='Date Set user', blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    image = models.ForeignKey(ImageUsers, on_delete=models.CASCADE, blank=True)


    # def save(self, *args, **kwargs):
    #     dataset =''
    #     validated_data = self.image
    #     for image_data in validated_data.get('image'):
    #         link = f'{image_data.image_user}'.split('/')[0].lower()
    #         links = f'{image_data.image_user}'.split('/')[1]
    #         face_img = face_recognition.load_image_file(f"media/{link}/{links}")
    #         face_enc = face_recognition.face_encodings(face_img)[0]
    #         dataset += f'{face_enc}'
    #     return super(CustomUser).save(dataset)


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

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'Stories'
