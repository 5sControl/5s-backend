from rest_framework import serializers

from src.Inventory.models import Items
from src.Suppliers.models import Suppliers

from src.Suppliers.serializers import SuppliersSerializer


class ItemsSerializer(serializers.ModelSerializer):
    """Serializer for Items model"""

    suppliers = SuppliersSerializer(many=False, required=False)

    class Meta:
        model = Items
        fields = ['id', 'name', 'status', 'current_stock_level', 'low_stock_level', 'camera',
                  'date_created', 'date_updated', 'coords', 'prev_status', 'multi_row',
                  'order_quantity', 'suppliers']

    def create(self, validated_data):
        suppliers_data = validated_data.pop('suppliers', None)
        item = Items.objects.create(**validated_data)

        if suppliers_data:
            Suppliers.objects.create(item=item, **suppliers_data)

        return item

    def update(self, instance, validated_data):
        suppliers_data = validated_data.pop('suppliers', None)
        item = super().update(instance, validated_data)

        if suppliers_data:
            suppliers_serializer = SuppliersSerializer(instance.suppliers, data=suppliers_data)
            suppliers_serializer.is_valid(raise_exception=True)
            suppliers_serializer.save()

        return item
