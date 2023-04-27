from django.db import models


class DatabaseConnection(models.Model):
    database_type = models.CharField(max_length=50, default="OrderView", blank=False, null=False)
    server = models.CharField(max_length=200, blank=False, null=False)
    database = models.CharField(max_length=200, blank=False, null=False)
    username = models.CharField(max_length=200, blank=False, null=False)
    password = models.CharField(max_length=500, blank=False, null=False)
    port = models.IntegerField(default=1433, blank=False, null=False)
