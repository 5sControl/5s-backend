from django.db import models
from django_countries.fields import CountryField


class Suppliers(models.Model):
    """Models Suppliers"""

    name_company = models.TextField(verbose_name="Name of company suppliers")

    first_address = models.CharField(max_length=100, verbose_name="Lega address of company supplier", blank=True,
                                     null=True)
    second_address = models.CharField(max_length=100, verbose_name="Physical address of company supplier", blank=True,
                                      null=True)
    country = CountryField(verbose_name="Country of company suppliers", blank=True, null=True)
    state = models.CharField(max_length=50, verbose_name="State of company suppliers", blank=True, null=True)
    city = models.CharField(max_length=50, verbose_name="City of company suppliers", blank=True, null=True)
    website = models.TextField(verbose_name="Website of suppliers")
    contact_email = models.EmailField(verbose_name="Contact email suppliers", blank=True, null=True)
    contact_phone = models.TextField(verbose_name="Contact phone number suppliers", blank=True, null=True)
    contact_mobile_phone = models.TextField(verbose_name="Contact mobile phone number suppliers", blank=True, null=True)
    logo = models.ImageField(verbose_name="Logo company", blank=True, null=True)
    file = models.FileField(verbose_name="File to send notification", blank=True, null=True)
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    date_edited = models.DateTimeField(verbose_name="Date edited", auto_now=True)

    def __str__(self):
        return self.name_company
