from rest_framework import serializers

from src.Inventory.models import Items

from src.Suppliers.serializers import SuppliersSerializer


class ItemsSerializer(serializers.ModelSerializer):
    """
    Items Serializer
    """

    suppliers = SuppliersSerializer(many=False)

    class Meta:
        model = Items
        fields = ["id",
                  "name",
                  "status",
                  "current_stock_level",
                  "low_stock_level",
                  "camera",
                  "date_created",
                  "date_updated",
                  "coords",
                  "multi_row",
                  "order_quantity",
                  "suppliers"
                  ]
