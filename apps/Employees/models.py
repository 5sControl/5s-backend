from django.db import models
from apps.Locations.models import Location

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
    
    # def create(self, validated_data):

    #     if validated_data['image']:
    #         face_img = face_recognition.load_image_file(f"{validated_data['image']}")
    #         dataset = face_recognition.face_encodings(face_img)[0]
    #         print('[INFO] Finded dataset')

    #         first_name = validated_data['first_name']
    #         last_name = validated_data['last_name']
    #         date_joined = validated_data['date_joined']
    #         image = validated_data['image']
    #         status = validated_data['status']
    #         custom_user = CustomUser.objects.create(first_name=first_name, last_name=last_name,
    #                                                 date_joined=date_joined, image=image, status=status)
    #         print('[INFO] Successfully created record')

    #         return custom_user


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
    image = models.CharField(verbose_name='Image', blank=True, null=True, max_length=200)

    def __str__(self):
        return f'{self.location}'

    class Meta:
        verbose_name = 'History'
        verbose_name_plural = 'History'
