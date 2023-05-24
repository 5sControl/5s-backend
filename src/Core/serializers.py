from rest_framework import serializers

from src.Core.models import SystemMessage


class SystemMessagesSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S.%f", required=False)

    class Meta:
        model = SystemMessage
        fields = [
            "title",
            "content",
            "created_at",
        ]
