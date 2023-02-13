from django.db import models

from ..Employees.models import CustomUser
from ..Locations.models import Location
from ..Locations.models import Camera

from django.utils.safestring import mark_safe


class History(models.Model):
    people = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="people_in_location",
    )
    location = models.ForeignKey(
        Location,
        related_name="Location_users",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    entry_date = models.DateTimeField(auto_now_add=True)
    release_date = models.DateTimeField(blank=True, null=True)
    image = models.CharField(
        verbose_name="Image", blank=True, null=True, max_length=200
    )
    camera = models.ForeignKey(
        Camera, on_delete=models.CASCADE, verbose_name="NameCamera"
    )
    name_file = models.CharField(
        verbose_name="name_file", blank=True, null=True, max_length=100
    )
    action = models.CharField(
        verbose_name="action camera", blank=True, null=True, max_length=50
    )

    @property
    def image_preview(self):
        if self.image:
            return mark_safe(
                '<img src="{}" width="450" height="300" />'.format(self.image.url)
            )
        return ""

    def __str__(self):
        return f"{self.location}"

    class Meta:
        verbose_name = "History"
        verbose_name_plural = "History"
