from rest_framework import serializers
from src.Mailer.models import SMTPSettings, Emails, WorkingTime, DayOfWeek


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
    time_start = serializers.TimeField()
    time_end = serializers.TimeField()

    class Meta:
        model = WorkingTime
        fields = ['id', 'time_start', 'time_end', 'days_of_week']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['days_of_week'] = list(instance.days_of_week.values_list('day', flat=True))
        return representation
