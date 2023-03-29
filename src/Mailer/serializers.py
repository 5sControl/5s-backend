from rest_framework import serializers
from src.Mailer.models import SMTPSettings


class SMTPSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSettings
        fields = '__all__'


class EmailSerializer(serializers.Serializer):
    to_email = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()
