from rest_framework import serializers
from src.ReportsAI.models import ExtensionReport


class ExtensionReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtensionReport
        fields = '__all__'
