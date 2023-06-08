from rest_framework import serializers

from src.Suppliers.models import Suppliers

from django_countries.serializer_fields import CountryField


class SuppliersSerializer(serializers.ModelSerializer):

    name_company = serializers.CharField(allow_blank=True)
    website = serializers.CharField(allow_blank=True)
    country = CountryField()

    class Meta:
        model = Suppliers
        fields = '__all__'
        read_only_fields = ["id", "date_joined", "date_edited"]
