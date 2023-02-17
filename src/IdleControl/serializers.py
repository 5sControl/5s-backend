from rest_framework import serializers
from src.IdleControl.models import Actions, Photos


class PhotoSerializers(serializers.ModelSerializer):
    """All photos on IdleControl"""

    class Meta:
        model = Photos
        fields = ["id", "image", "idle_id"]


class IdleControlSerializers(serializers.ModelSerializer):
    """Reports on IdleControl"""

    photos = PhotoSerializers(many=True, read_only=True)

    class Meta:
        model = Actions
        fields = ['id', 'camera', 'start_tracking', 'stop_tracking', 'date_created', 'photos']

