from django.contrib import admin

from .models import History

from ..Employees.models import StaffControlUser

from django.utils.safestring import mark_safe


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = (
        "people",
        "entry_date",
        "release_date",
        "action",
        "location",
        "image_tag",
    )
    list_filter = ("people", "location", "id", "entry_date", "action")
    readonly_fields = (
        "people",
        "entry_date",
        "release_date",
        "action",
        "location",
        "image_tags",
    )

    def location(self, obj):
        result = StaffControlUser.objects.filter(id=obj.people.id).values(
            "location_id"
        )[0]["location_id"]
        return result

    def dataset(self, obj):
        result = StaffControlUser.objects.filter(id=obj.people.id).values("dataset")[0][
            "dataset"
        ]
        return result

    def image_tag(self, obj):
        return mark_safe(f'<img src="/{obj.image}" width="50px" height="60px" />')

    def image_tags(self, obj):
        return mark_safe(f'<img src="/{obj.image}" width="400px" height="400px" />')
