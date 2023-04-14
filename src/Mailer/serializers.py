from rest_framework import serializers
from src.Mailer.models import SMTPSettings, Emails, WorkingTime


class SMTPSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSettings
        fields = '__all__'


class EmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ['id', 'email', 'is_active', ]


class WorkingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingTime
        fields = '__all__'
