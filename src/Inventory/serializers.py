from rest_framework import serializers

from src.Inventory.models import Items


class ItemsSerializer(serializers.ModelSerializer):
    """Serializer for Items model"""

    class Meta:
        model = Items
        fields = ['id', 'name', 'status', 'current_stock_level', 'low_stock_level', 'camera',
                  'date_created', 'date_updated', 'coords', 'prev_status', 'multi_row',
                  'order_quantity', 'suppliers']
