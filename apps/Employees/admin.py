from django.contrib import admin
from .models import CustomUser, History


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'date_joined', 'location')
    list_filter = ("username", 'id')


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('people', 'id', 'location', 'entry_data', 'release_data', 'dataset_user', 'image')
    list_filter = ('people', 'id')
