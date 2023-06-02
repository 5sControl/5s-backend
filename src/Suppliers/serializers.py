from rest_framework import serializers
from src.Suppliers.models import Suppliers


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'
