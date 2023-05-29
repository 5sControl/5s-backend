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

    def create(self, validated_data):
        email = validated_data.get('email')
        if Emails.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return super().create(validated_data)


class WorkingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingTime
        fields = '__all__'
