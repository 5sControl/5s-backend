from django.db import models


class DatabaseConnection(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    user = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    host = models.CharField(max_length=100, blank=False, null=False, unique=True)
