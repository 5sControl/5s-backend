from rest_framework import serializers

from src.Cameras.serializers import CameraSerializer
from src.Reports.serializers import ReportSerializers

from src.Inventory.models import Items


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["id",
                  "name",
                  "status",
                  "current_stock_level",
                  "low_stock_level",
                  "email",
                  "camera",
                  "report",
                  "date_created"]


# class HistoryItemSerializer(serializers.Serializer):
#     """All history on reports and items"""
#
#     camera = CameraSerializer(many=False)
#     report = ReportSerializers(many=False)
#
#     class Meta:
#         model = Items
#         fields = []
