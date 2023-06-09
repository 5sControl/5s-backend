from rest_framework import serializers


from django_countries.serializer_fields import CountryField

from src.CompanyLicense.models import Company


class SuppliersSerializer(serializers.ModelSerializer):
    country = CountryField(allow_null=True)

    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ["my_company"]


class CountrySerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
