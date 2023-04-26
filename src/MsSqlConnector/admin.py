from django.contrib import admin

from .models import DatabaseConnection


@admin.register(DatabaseConnection)
class DatabaseConnectionAdmin(admin.ModelAdmin):
    list_display = ("database_type", "server", "database", "username", "password")
