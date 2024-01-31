from django.contrib import admin
from src.Extension.models import ExtensionReport


@admin.register(ExtensionReport)
class ExtensionReportAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'extension_user', 'user_name')
    list_filter = ('project_id', 'extension_user')

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        allowed_user_id = 7
        if allowed_user_id == request.user.id:
            for model in admin.site._registry.copy():
                if model != ExtensionReport:
                    admin.site.unregister(model)
        return True
