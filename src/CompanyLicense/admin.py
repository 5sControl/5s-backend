from django.contrib import admin
from .models import License, Company


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_filter = ("id",)
    readonly_fields = (
        'license_key',
        'date_joined',
        'valid_until',
        'is_active',
        'count_cameras',
        'neurons_active'
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name_company",
        "city",
        "state",
        "website",
        "contact_email",
        "contact_phone",
        "contact_mobile_phone",
        "logo",
        "file",
        "date_joined",
        "date_edited",
    )
