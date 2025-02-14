from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models

from datetime import timedelta
import random
import string


class CustomUser(AbstractUser):
    ADMIN = 'admin'
    SUPERUSER = 'superuser'
    WORKER = 'worker'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (SUPERUSER, 'Superuser'),
        (WORKER, 'Worker'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=WORKER)
    workplace_id = models.IntegerField(blank=True, null=True, default=None)
    email = models.EmailField(blank=True, unique=True, default="")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        db_table = "custom_user"


class PasswordResetCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.code = self.generate_code()
            self.expires_at = now() + timedelta(minutes=15)
        super().save(*args, **kwargs)
