from django.contrib import admin
from .models import CustomUser, History
from django.utils.safestring import mark_safe


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'first_name', 'last_name', 'date_joined', 'location')
    list_filter = ("username", 'id')


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('people', 'id', 'location', 'entry_date', 'release_date', 'dataset_user', 'get_image')
    list_filter = ('people', 'id')
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url} "width="50" height="60" />')

    get_image.short_description = 'image'
