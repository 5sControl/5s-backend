from django.contrib import admin

from .models import ConnectionInfo


@admin.register(ConnectionInfo)
class ConnectionInfoAdmin(admin.ModelAdmin):
    list_display = (
        "type",
        "dbms",
        "is_active",
        "server",
        "database",
        "username",
        "password",
        "port",
        "host",
    )
