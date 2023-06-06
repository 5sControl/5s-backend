from rest_framework import serializers

from src.Reports.models import Report, SkanyReport
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


class OperationReportSerializer(serializers.ModelSerializer):
    operationID = serializers.IntegerField(source='skany_index')
    camera_ip = serializers.CharField(source='report.camera')
    startTime = serializers.FloatField(source='operation_time')

    class Meta:
        model = SkanyReport
        fields = ['id', 'operationID', 'camera_ip', 'startTime']
