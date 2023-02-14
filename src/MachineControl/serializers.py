from rest_framework import serializers
from models import Action


class MachineControlSerializers(serializers.ModelSerializer):
    """Reports on MachineControl"""

    class Meta:
        model = Action
        fields = ["id", "camera", "photo_start", "photo_stop", "start_tracking", "stop_tracking"]

