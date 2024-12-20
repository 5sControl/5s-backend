from django.contrib import admin
from .models.camera import Camera, ZoneCameras
from .models.algorithm import Algorithm, CameraAlgorithm, CameraAlgorithmLog


@admin.register(Camera)
class CamerasAdmin(admin.ModelAdmin):
    list_filter = ("id",)


@admin.register(Algorithm)
class AlgorithmAdmin(admin.ModelAdmin):
    list_filter = ("download_status", "name", "used_in")
    list_display = ("name", "used_in", "image_name", "download_status", "id")


@admin.register(CameraAlgorithm)
class CameraAlgorithmAdmin(admin.ModelAdmin):
    list_filter = ("id", "algorithm", "camera")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


@admin.register(CameraAlgorithmLog)
class CameraAlgorithmLogAdmin(admin.ModelAdmin):
    list_filter = ("id",)


@admin.register(ZoneCameras)
class ZoneCamerasAdmin(admin.ModelAdmin):
    readonly_fields = ["is_active", "camera", "workplace"]
    list_display = (
        "camera",
        "name",
        "id",
        "coords",
        "workplace",
        "index_workplace",
        "date_created",
        "date_updated",
    )
