from django.contrib import admin
from src.newOrderView.models import FiltrationOperationsTypeID


@admin.register(FiltrationOperationsTypeID)
class FiltrationOperationsAdmin(admin.ModelAdmin):
    list_display = ("operation_type_id", "type_erp", "name", "is_active", "id")
