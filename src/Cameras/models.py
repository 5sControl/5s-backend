from django.db import models


class Camera(models.Model):
    """Model for saving camera information"""

    id = models.CharField(primary_key=True, max_length=30)
    name = models.CharField(max_length=100, blank=True, null=True)

    username = models.CharField(max_length=100, default="admin", blank=True, null=True)
    password = models.CharField(max_length=250, default="admin", blank=True, null=True)
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

