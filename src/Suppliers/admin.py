from django.contrib import admin
from .models import Suppliers


@admin.register(Suppliers)
class SuppliersAdmin(admin.ModelAdmin):
    list_filter = ("id",)
    list_display = (
        'name_company',
        'city',
        'state',
        'website',
        'contact_email',
        'contact_phone',
        'contact_mobile_phone',
        'logo',
        'file',
        'date_joined',
        'date_edited'
    )
