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

    date_created = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)
    date_updated = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)
    stop_tracking = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)
    start_tracking = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)

    def get_extra(self, obj):
        extra = obj.extra
        item_id = self.context.get('item_id')
        if item_id:
            filtered_extra = [item for item in extra if item.get('itemId') == item_id]
        else:
            filtered_extra = obj.extra
        return filtered_extra


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


class SearchReportSerializers(serializers.ModelSerializer):
    """Report search items"""

    photos = PhotoSerializers(many=True)
    algorithm = serializers.SerializerMethodField()

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

    date_created = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)
    date_updated = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)
    stop_tracking = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)
    start_tracking = serializers.DateTimeField("%Y-%m-%d %H:%M:%S.%fZ", required=False)

    def get_algorithm(self, obj):
        return obj.algorithm.name if obj.algorithm else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        extra = data.pop('extra', [])
        item_id = self.context.get('item_id')

        filtered_extra = []
        for item in extra:
            if item and isinstance(item, dict) and item.get('itemId') == item_id:
                filtered_extra.append(item)

        if filtered_extra:
            data.update({key: value for item in filtered_extra for key, value in item.items()})

        return data if filtered_extra else None
