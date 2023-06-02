from rest_framework import serializers
from src.Suppliers.models import Suppliers


class SuppliersSerializer(serializers.ModelSerializer):

    name_company = serializers.CharField(allow_blank=True)
    website = serializers.CharField(allow_blank=True)

    class Meta:
        model = Suppliers
        fields = '__all__'
