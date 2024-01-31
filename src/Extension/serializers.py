from rest_framework import serializers
from src.Extension.models import ExtensionReport


class ExtensionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtensionReport
        fields = '__all__'
