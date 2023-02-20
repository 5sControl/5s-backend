from rest_framework import serializers
from src.Reports.models import Report
from src.Image.serializers import PhotoSerializers


class ReportSerializers(serializers.ModelSerializer):
    """All photos on Reports"""

    photos = PhotoSerializers(many=True)

    class Meta:
        model = Report
        fields = ["id", "algorithm", "camera", "start_tracking",
                  "stop_tracking", "violation_found", "extra", "date_created", "photos"]



