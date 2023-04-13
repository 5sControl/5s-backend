from django.contrib import admin
from .models import Report, SkanyReport
from src.ImageReport.models import Image
from django.utils.safestring import mark_safe



# @admin.register(Report)
# class ReportAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "algorithm",
#         "camera",
#         "start_tracking",
#         "stop_tracking",
#         "violation_found",
#         "date_created",
#     )
#     list_filter = ("algorithm", "camera",)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 0
    readonly_fields = ['preview']

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image}" width="150px" height="120px" />')
    preview.short_description = 'Preview'


class ReportAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ['algorithm', 'id', 'camera', 'violation_found', 'date_created']
    list_filter = ['algorithm', 'camera', 'violation_found']
    search_fields = ['algorithm__name', 'camera__name']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('photos')
        return queryset


admin.site.register(Report, ReportAdmin)


@admin.register(SkanyReport)
class SkanyReportAdmin(admin.ModelAdmin):
    list_display = ("report", "skany_index")
