from rest_framework import serializers

from src.Inventory.models import Items


class ItemsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Items
        fields = [
            "id",
            "name",
            "object_type",
            "status",
            "current_stock_level",
            "low_stock_level",
            "camera",
            "date_created",
            "date_updated",
            "coords",
            "prev_status",
            "order_quantity",
            "suppliers",
            "to_emails",
            "copy_emails",
            "subject",
        ]
