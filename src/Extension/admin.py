from django.contrib import admin
from src.Extension.models import ExtensionReport


@admin.register(ExtensionReport)
class ExtensionReportAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'extension_user', 'user_name', 'created_at')
    list_filter = ('project_id', 'extension_user', 'created_at')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
