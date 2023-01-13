from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'image_preview',)
    list_filter = ('id', 'status', 'date_joined')
    readonly_fields =('first_name', 'last_name', 'image_preview', 'status', 'date_joined')
        
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True
