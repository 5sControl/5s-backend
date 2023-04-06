from rest_framework import serializers
from src.Mailer.models import SMTPSettings, Messages


class SMTPSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSettings
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    recipients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Messages
        fields = ['id', 'subject', 'message', 'is_send', 'date_created', 'date_updated', 'recipients']
