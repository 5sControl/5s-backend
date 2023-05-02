from django.contrib import admin
from .models import Camera


@admin.register(Camera)
class CamerasAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "username",
        "password",
        "is_active",
    )
    list_filter = ("id",)
