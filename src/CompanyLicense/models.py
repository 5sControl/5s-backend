from django.utils import timezone

from django.db import models

from django_countries.fields import CountryField


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
    """Models my company"""

    name_company = models.TextField(verbose_name="Name of my company")

    first_address = models.CharField(max_length=100, verbose_name="Lega address of my company", blank=True,
                                     null=True)
    second_address = models.CharField(max_length=100, verbose_name="Physical address of my company", blank=True,
                                      null=True)
    country = CountryField(verbose_name="Country of my company", blank=True, null=True)
    state = models.CharField(max_length=50, verbose_name="State of my company", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="City of my company", blank=True, null=True)
    website = models.TextField(verbose_name="Website of suppliers", blank=True, null=True)
    contact_email = models.EmailField(verbose_name="Contact email suppliers")
    contact_phone = models.TextField(verbose_name="Contact phone number suppliers", blank=True, null=True)
    contact_mobile_phone = models.TextField(verbose_name="Contact mobile phone suppliers", blank=True, null=True)
    logo = models.ImageField(verbose_name="Logo suppliers", blank=True, null=True)
    file = models.FileField(verbose_name="File to send notification", blank=True, null=True)
    index = models.IntegerField(verbose_name="Postcode", blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date edited", auto_now=True)
    my_company = models.BooleanField(default=False)

    def __str__(self):
        return self.name_company
