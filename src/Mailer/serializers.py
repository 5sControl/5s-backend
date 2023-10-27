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


class DayOfWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = DayOfWeek
        fields = '__all__'


class WorkingTimeSerializer(serializers.ModelSerializer):
    time_start = serializers.TimeField()
    time_end = serializers.TimeField()
    days_of_week = DayOfWeekSerializer(many=True, required=False)

    class Meta:
        model = WorkingTime
        fields = ['id', 'time_start', 'time_end', 'days_of_week']

    def create(self, validated_data):
        if validated_data.get('days_of_week'):
            days_of_week_data = validated_data.pop('days_of_week')
            working_time = WorkingTime.objects.create(**validated_data)

            for day_data in days_of_week_data:
                day, created = DayOfWeek.objects.get_or_create(**day_data)
                working_time.days_of_week.add(day)

            return working_time
        else:
            working_time = WorkingTime.objects.create(**validated_data)
            return working_time

