from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = (
        "id", "algorithm", "camera", "start_tracking", "stop_tracking", "violation_found", "date_created", )
    list_filter = ("id",)
