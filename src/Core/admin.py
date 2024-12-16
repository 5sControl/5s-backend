from django.contrib import admin

from src.Core.models import SystemMessage, CustomPermission


@admin.register(CustomPermission)
class CustomPermissionAdmin(admin.ModelAdmin):
    list_display = ('codename', 'name')
    search_fields = ('codename', 'name')


@admin.register(SystemMessage)
class SystemMessageAdmin(admin.ModelAdmin):
    list_display = ["content", "title", "created_at"]
    list_filter = ["title"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False
