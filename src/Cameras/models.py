from django.db import models

from django.core.validators import RegexValidator

# from django.contrib.auth.hashers import make_password


class Camera(models.Model):
    """Model for saving camera information"""

    id = models.CharField(
        primary_key=True,
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                message="ID must be a valid IP address",
            )
        ],
    )
    name = models.CharField(max_length=100, blank=True, null=True)

    username = models.CharField(max_length=100, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.id
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Camera"
        verbose_name_plural = "Cameras"
