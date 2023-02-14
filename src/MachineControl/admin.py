from django.contrib import admin
from .models import MachineAction


@admin.register(MachineAction)
class MachineAdmin(admin.ModelAdmin):
    list_display = ("id", "camera", "photo_start", "photo_stop", "start_tracking", "stop_tracking")
    list_filter = ("id",)

