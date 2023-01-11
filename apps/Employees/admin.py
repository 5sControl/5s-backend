from django.contrib import admin
from .models import CustomUser, History
from apps.Locations.models import Location
from django.utils.safestring import mark_safe
from django.utils.html import format_html


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'id', 'last_name', 'date_joined', 'status', 'image_tag']
    list_filter = ('id',)
    readonly_fields = ['image_tag']

    # def image_tag(self, obj):
    #     return format_html('<img src="{}" width="auto" height="200px" />'.format(obj.img.url))
    #
    # image_tag.short_description = 'Image'

    def image_tag(self, obj):

        return mark_safe(f'<img src="{obj.image.url}" width="50px" height="60px" />')

    # image_tag.short_description = 'image'


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ('people', 'id', 'entry_date', 'release_date', 'get_image', 'location')
    list_filter = ('people', 'id')
    readonly_fields = ("get_image",)

    def location(self, obj):
        result = CustomUser.objects.filter(id=obj.people.id).values('location_id')[0]['location_id']
        return result

    def dataset(self, obj):
        result = CustomUser.objects.filter(id=obj.people.id).values('dataset')[0]['dataset']
        return result

    def get_image(self, obj):
        return mark_safe(f'<img src="{obj.image.url} "width="50" height="60" />')

    get_image.short_description = 'image'
