from django.db import models

from src.Reports.models import Report


class DatabaseConnection(models.Model):
    database_type = models.CharField(
        max_length=50, default="OrderView", blank=False, null=False
    )
    server = models.CharField(max_length=20, blank=False, null=False)
    database = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(
        max_length=200, blank=False, null=False
    )  # TODO: should be hashed


# TODO
class Skany_Vs_Reports(models.Model):
    report = models.ForeignKey(
        Report, on_delete=models.CASCADE, blank=False, null=False
    )
    skany_indeks = models.CharField(max_length=50, blank=False, null=False)
