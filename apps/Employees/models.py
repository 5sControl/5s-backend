from django.db import models
from apps.Locations.models import Location

from django.utils.safestring import mark_safe


class CustomUser(models.Model):
    """Employee"""

    first_name = models.CharField(default='Unknown', max_length=40, blank=True, null=True)
    last_name = models.CharField(default='Unknown', max_length=40, blank=True, null=True)
    dataset = models.TextField(verbose_name='Date Set user', blank=True, null=True)
    image1 = models.ImageField(upload_to="", verbose_name='photo below')
    image2 = models.ImageField(upload_to="", verbose_name='photo from above')
    image3 = models.ImageField(upload_to="", verbose_name='photo in the center')
    image4 = models.ImageField(upload_to="", verbose_name='photo on the left')
    image5 = models.ImageField(upload_to="", verbose_name='photo on the right')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True, related_name='location')
    status = models.BooleanField(verbose_name='Status in location', default=False,)
    date_joined = models.DateTimeField(auto_now_add=True)

    @property
    def image_preview(self):
        if self.image3:
            return mark_safe('<img src="{}" width="450" height="300" />'.format(self.image3.url))
        return ""

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employers'
