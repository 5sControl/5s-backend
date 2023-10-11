from rest_framework import serializers

from src.Reports.models import Report, SkanyReport
from src.ImageReport.serializers import PhotoSerializers
from src.CameraAlgorithms.serializers import AlgorithmSerializer, CameraReportSerializer

from datetime import datetime


class ReportSerializers(serializers.ModelSerializer):
    """All photos on Reports"""

    photos = PhotoSerializers(many=True)
    algorithm = AlgorithmSerializer(many=False)
    camera = CameraReportSerializer(many=False)
    stop_tracking = serializers.SerializerMethodField()
    start_tracking = serializers.SerializerMethodField()
    extra = serializers.SerializerMethodField()

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

    date_created = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%f %z", required=False)
    date_updated = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%f %z", required=False)

    def get_extra(self, obj):
        extra = obj.extra
        item_id = self.context.get('item_id')
        if item_id:
            filtered_extra = [item for item in extra if item.get('itemId') == item_id]
        else:
            filtered_extra = obj.extra
        return filtered_extra

    def get_stop_tracking(self, obj):
        if obj.stop_tracking:
            formatted_date = datetime.strptime(obj.stop_tracking, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S.%f %z"
            )
            return formatted_date + "+0000"
        return None

    def get_start_tracking(self, obj):
        if obj.start_tracking:
            formatted_date = datetime.strptime(obj.start_tracking, "%Y-%m-%d %H:%M:%S.%f").strftime(
                "%Y-%m-%d %H:%M:%S.%f %z"
            )
            return formatted_date + "+0000"
        return None


class OperationReportSerializer(serializers.ModelSerializer):
    operationID = serializers.IntegerField(source="skany_index")
    camera_ip = serializers.CharField(source="report.camera")
    startTime = serializers.IntegerField(source="start_time")
    endTime = serializers.IntegerField(source="end_time")

    class Meta:
        model = SkanyReport
        fields = ["id", "operationID", "camera_ip", "startTime", "endTime"]


class ReportByIDSerializer(serializers.ModelSerializer):
    algorithm = AlgorithmSerializer()
    camera = serializers.StringRelatedField()

    class Meta:
        model = Report
        fields = [
            "id",
            "start_tracking",
            "stop_tracking",
            "violation_found",
            "extra",
            "status",
            "algorithm",
            "camera",
        ]
