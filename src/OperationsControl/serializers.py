from rest_framework import serializers
from src.OperationsControl.models import OperationsCounter


class OperationControlSerializers(serializers.ModelSerializer):
    """Counter operations"""

    class Meta:
        model = OperationsCounter
        fields = ["id", "date_time", "date_created"]
