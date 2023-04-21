from django.db import models


class DatabaseConnection(models.Model):
    database_type = models.CharField(
        max_length=50, default="OrderView", blank=False, null=False
    )
    server = models.CharField(max_length=300, blank=False, null=False)
    database = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(
        max_length=200, blank=False, null=False
    )  # TODO: should be hashed
