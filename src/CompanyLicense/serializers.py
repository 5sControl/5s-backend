from rest_framework import serializers

from src.CompanyLicense.models import License
from src.CompanyLicense.service import decrypt_string

import datetime
from django.utils import timezone


class CompanySerializer(serializers.Serializer):
    license_key = serializers.CharField(required=True, write_only=True)

    def create(self, validated_data):
        valid_data = decrypt_string(validated_data["license_key"])
        valid_date = datetime.datetime.strptime(
            valid_data["valid_until"], "%Y-%m-%d"
        ).date()
        if valid_date >= timezone.now().date():
            data = {
                "license_key": validated_data["license_key"],
                "name_company": valid_data["name_company"],
                "count_cameras": valid_data["count_cameras"],
                "neurons_active": valid_data["neurons_active"],
                "is_active": True,
                "valid_until": valid_date,
            }

            company = License.objects.create(**data)

            return company

        raise serializers.ValidationError({"message": "You have an outdated license"})

    def validate(self, data):
        try:
            valid_data = decrypt_string(data["license_key"])
        except Exception as e:
            raise serializers.ValidationError({"error": str(e)})
        return data
