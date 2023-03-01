from django.contrib import admin
from .models import Company


@admin.register(Company)
class CamerasAdmin(admin.ModelAdmin):
    list_filter = ("id",)
