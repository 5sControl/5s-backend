from django.contrib import admin
from src.ReportsAI.models import ExtensionReport


class ExtensionReportAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'extension_user', 'ai_comments', 'user_name', 'text_comment')
    list_filter = ('project_id', 'extension_user')

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(ExtensionReport, ExtensionReportAdmin)
