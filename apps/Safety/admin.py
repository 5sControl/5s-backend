from django.contrib import admin
from .models import Action


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'action', 'name_file', 'camera', 'date_created')
    list_filter = ('id', 'image', 'action', 'name_file', 'camera', 'date_created')
