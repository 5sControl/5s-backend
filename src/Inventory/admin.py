from django.contrib import admin
from src.Inventory.models import Items


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = (
        "name", "id", "suppliers", "order_quantity", "status", "current_stock_level", "low_stock_level", "camera",
        "date_updated", "coords", "multi_row", "suppliers", "order_quantity", 'to_emails', 'copy_emails', 'subject')
    list_filter = ("status", "current_stock_level", "low_stock_level", "camera", "multi_row")
