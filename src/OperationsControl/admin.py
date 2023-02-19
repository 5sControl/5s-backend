from django.contrib import admin
from .models import OperationsCounter


@admin.register(OperationsCounter)
class OperationsAdmin(admin.ModelAdmin):
    list_display = ("id", "date_time", "date_created")
    list_filter = ("id",)
