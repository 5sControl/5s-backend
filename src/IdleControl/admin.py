from django.contrib import admin
from .models import Actions


@admin.register(Actions)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'camera', 'start_tracking', 'stop_tracking')
    list_filter = ("id",)

