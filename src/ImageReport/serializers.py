from rest_framework import serializers
from src.ImageReport.models import Image


class PhotoSerializers(serializers.ModelSerializer):
    """All photos on IdleControl"""

    class Meta:
        model = Image
        fields = ["id", "image", "date", "report_id"]
