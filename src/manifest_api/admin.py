from django.contrib import admin
from src.manifest_api.models import ManifestConnection


@admin.register(ManifestConnection)
class ManifestConnectionAdmin(admin.ModelAdmin):
    list_display = ["host", "status"]
    readonly_fields = ["host", "username", "token", "password"]
