from django.contrib import admin
from .models import License


@admin.register(License)
class CamerasAdmin(admin.ModelAdmin):
    list_filter = ("id",)
    readonly_fields = (
        'license_key',
        'name_company',
        'date_joined',
        'valid_until',
        'is_active',
        'count_cameras',
        'neurons_active'
    )
