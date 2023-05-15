from rest_framework import serializers

from src.Reports.models import Report
from src.ImageReport.serializers import PhotoSerializers
from src.CameraAlgorithms.serializers import AlgorithmSerializer, CameraReportSerializer


class ReportSerializers(serializers.ModelSerializer):
    """All photos on Reports"""

    photos = PhotoSerializers(many=True)
    algorithm = AlgorithmSerializer(many=False)
    camera = CameraReportSerializer(many=False)

    class Meta:
        model = Report
        fields = [
            "id",
            "algorithm",
            "camera",
            "start_tracking",
            "stop_tracking",
            "violation_found",
            "extra",
            "date_created",
            "photos",
            "date_updated",
            "status",
        ]
