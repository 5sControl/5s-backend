from django.contrib import admin
from .models import Cameras, Gate, Location


@admin.register(Cameras)
class CamerasAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    list_filter = ("name", 'id')


@admin.register(Gate)
class GatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'camera_input', 'camera_output')
    list_filter = ("name", 'id')


@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'people_id', 'gate_id')
    list_filter = ("name", 'id')
