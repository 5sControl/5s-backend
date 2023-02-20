from rest_framework import serializers
from src.Image.models import Photos


class PhotoSerializers(serializers.ModelSerializer):
    """All photos on IdleControl"""

    class Meta:
        model = Photos
        fields = ["id", "image", "date", "report_id"]



