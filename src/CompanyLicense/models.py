from django.utils import timezone
from django.db import models


class License(models.Model):
    """License of company"""

    license_key = models.TextField(verbose_name="Company license key")
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date edited", auto_now=True)
    valid_until = models.DateField(verbose_name="Date which license is active")
    is_active = models.BooleanField(verbose_name="Is active license", default=False)
    count_cameras = models.IntegerField(verbose_name="Count of cameras in active")
    neurons_active = models.IntegerField(verbose_name="Count of active neurons")

    def is_valid(self):
        return self.valid_until >= timezone.now().date()

    def __str__(self):
        return f"Number of days until license expires: {self.valid_until - timezone.now().date()}"

    class Meta:
        verbose_name = "License"
        verbose_name_plural = "Licenses"


class Company(models.Model):
    """Models company"""

    name_company = models.TextField(verbose_name="Name of company")
    address_company = models.TextField(verbose_name="Address of company")
    contact_email = models.EmailField(verbose_name="Contact email")
    contact_phone = models.TextField(verbose_name="Contact phone number")
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date edited", auto_now=True)

    def __str__(self):
        return self.name_company
