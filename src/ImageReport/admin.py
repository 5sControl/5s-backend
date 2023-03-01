from django.contrib import admin
from .models import Image


@admin.register(Image)
class CamerasAdmin(admin.ModelAdmin):
    list_filter = ("id",)
