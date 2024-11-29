from django.contrib.auth.models import AbstractUser
from django.db import models
from django.apps import apps


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
    workplace_id = models.ForeignKey('erp_5s.ReferenceItems', null=True, on_delete=models.SET_NULL, default=None)

    class Meta:
        verbose_name = "Custom User"
        verbose_name_plural = "Custom Users"
        db_table = "custom_user"
