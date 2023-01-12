from django.contrib import admin
from .models import Camera, Gate, Location


@admin.register(Camera)
class CamerasAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ('id',)


@admin.register(Gate)
class GatesAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'camera_input', 'camera_output')
    list_filter = ("name", 'id')


@admin.register(Location)
class LocationsAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'gate_id')
    list_filter = ("name", 'id')
