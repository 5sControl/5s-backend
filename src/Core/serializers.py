from rest_framework import serializers

from src.Core.models import SystemMessage


class SystemMessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemMessage
        fields = [
            "title",
            "content"
        ]
