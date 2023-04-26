from django.db import models


class DatabaseConnection(models.Model):
    database_type = models.CharField(max_length=50, default="OrderView")
    server = models.CharField(max_length=200)
    database = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    port = models.IntegerField(default=1433)
