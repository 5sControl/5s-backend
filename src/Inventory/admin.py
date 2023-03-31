from django.contrib import admin
from src.Inventory.models import Items


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = (
        "name", "id", "status", "current_stock_level", "low_stock_level", "email", "camera", "date_updated", "coords")
    list_filter = ("name", "id", "status", "current_stock_level", "low_stock_level", "camera")
