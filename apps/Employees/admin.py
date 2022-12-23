from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'id',  'email', 'first_name', 'last_name', 'data_joined')
    list_filter = ("username", 'id')
