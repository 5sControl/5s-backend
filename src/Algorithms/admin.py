from django.contrib import admin

from .models import Algorithm, CameraAlgorithm, CameraAlgorithmLog


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "is_available",
    )
    list_filter = ("is_available",)


@admin.register(CameraAlgorithm)
class CameraAlgorithmAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "algorithm",
        "camera",
        "is_active",
        "process_id",
    )
    list_filter = ("camera", "process_id", "is_active")


@admin.register(CameraAlgorithmLog)
class CameraAlgorithmLogAdmin(admin.ModelAdmin):
    list_display = ("algorithm_name", "camera_ip", "created_at", "stoped_at",  "status")
    list_filter = ("algorithm_name", "camera_ip", "stoped_at", "created_at", "status")
