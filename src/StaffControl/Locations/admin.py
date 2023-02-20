from django.contrib import admin
from .models import Gate, Location


@admin.register(Gate)
class GatesAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "camera_input", "camera_output")
    list_filter = ("name", "id")


@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "gate_id")
    list_filter = ("name", "id")
