from rest_framework import serializers
from src.CompanyLicense.models import Company
from src.CompanyLicense.service import decrypt_string
import datetime


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["license_key"]

    def create(self, validated_data):
        valid_data = decrypt_string(validated_data["license_key"])
        data = {
            "license_key": validated_data["license_key"],
            "name_company": valid_data["name_company"],
            "count_cameras": valid_data["count_cameras"],
            "neurons_active": valid_data["neurons_active"],
            "valid_until": datetime.datetime.strptime(valid_data["valid_until"], '%Y-%m-%d').date(),
        }
        company = Company.objects.create(**data)
        return company
