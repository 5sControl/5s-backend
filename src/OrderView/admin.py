from django.contrib import admin
from .models import IndexOperations


@admin.register(IndexOperations)
class IndexOperationsAdmin(admin.ModelAdmin):
    list_display = ("type_operation", )
