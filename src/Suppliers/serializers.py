from rest_framework import serializers

from src.Suppliers.models import Suppliers

from django_countries.serializer_fields import CountryField


class SuppliersSerializer(serializers.ModelSerializer):
    country = CountryField(allow_null=True)

    class Meta:
        model = Suppliers
        fields = '__all__'
        read_only_fields = ["id", "date_joined", "date_edited"]


class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
