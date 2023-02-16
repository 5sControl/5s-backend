from rest_framework import serializers
from src.MachineControl.models import MachineAction


class MachineControlSerializers(serializers.ModelSerializer):
    """Reports on MachineControl"""

    class Meta:
        model = MachineAction
        fields = ["id", "camera", "photo_start", "photo_stop", "start_tracking", "stop_tracking", "date_created"]

