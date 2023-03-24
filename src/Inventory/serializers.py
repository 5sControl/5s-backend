import json

from rest_framework import serializers

from src.Inventory.models import Items


class ItemsSerializer(serializers.ModelSerializer):
    """
    Items Serializer
    """

    class Meta:
        model = Items
        fields = ["id",
                  "name",
                  "status",
                  "current_stock_level",
                  "low_stock_level",
                  "email",
                  "camera",
                  "date_created",
                  "date_updated",
                  "coords"
                  ]
