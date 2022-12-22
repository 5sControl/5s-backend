from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'date_set')
    list_filter = ("username", 'id')
    search_fields = ('id')
