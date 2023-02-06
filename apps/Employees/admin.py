from django.contrib import admin
from .models import CustomUser
from django.utils.html import mark_safe


@admin.register(CustomUser)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'image_tag1',)   # 'image_preview'
    list_filter = ('id', 'status', 'date_joined')
    readonly_fields = ('first_name', 'last_name', 'image_tag1', 'image_tag2', 'image_tag3',
                       'image_tag4', 'image_tag5', 'status', 'date_joined')

    def image_tag1(self, obj):
        return mark_safe(f'<img src="/images/{obj.image1}" width="150px" height="120px" />')

    def image_tag2(self, obj):
        return mark_safe(f'<img src="/images/{obj.image2}" width="150px" height="120px" />')

    def image_tag3(self, obj):
        return mark_safe(f'<img src="/images/{obj.image3}" width="150px" height="120px" />')

    def image_tag4(self, obj):
        return mark_safe(f'<img src="/images/{obj.image4}" width="150px" height="120px" />')

    def image_tag5(self, obj):
        return mark_safe(f'<img src="/images/{obj.image5}" width="150px" height="120px" />')

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True
