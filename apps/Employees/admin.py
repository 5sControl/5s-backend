from django.contrib import admin
from .models import CustomUser, History
from django.utils.safestring import mark_safe


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'image_preview',)
    list_filter = ('id', 'status', 'date_joined')
    readonly_fields =('first_name', 'last_name', 'image_preview', 'status', 'date_joined')
        
    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('people', 'entry_date', 'release_date', 'location')
    list_filter = ('people', 'location', 'id', 'entry_date',)
    readonly_fields = ('people', 'entry_date', 'release_date', 'location')

    def location(self, obj):
        result = CustomUser.objects.filter(id=obj.people.id).values('location_id')[0]['location_id']
        return result

    def dataset(self, obj):
        result = CustomUser.objects.filter(id=obj.people.id).values('dataset')[0]['dataset']
        return result

    def image_preview(self, obj):
        print(f'!!! {obj.image_preview}')
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True