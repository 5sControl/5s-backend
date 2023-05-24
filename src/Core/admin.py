from django.contrib import admin

from .models import SystemMessage


@admin.register(SystemMessage)
class SystemMessageAdmin(admin.ModelAdmin):
    list_filter = ["title"]
