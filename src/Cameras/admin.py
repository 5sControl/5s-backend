from django.contrib import admin
from .models import Camera


@admin.register(Camera)
class CamerasAdmin(admin.ModelAdmin):
    list_filter = ("id",)
