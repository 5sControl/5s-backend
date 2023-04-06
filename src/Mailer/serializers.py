from rest_framework import serializers
from src.Mailer.models import SMTPSettings, Messages, Recipients, Emails


class SMTPSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMTPSettings
        fields = '__all__'


class MessagesSerializer(serializers.ModelSerializer):
    recipients = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    to = serializers.ListField(child=serializers.EmailField())

    class Meta:
        model = Messages
        fields = ['id', 'subject', 'message', 'is_send', 'date_created', 'date_updated', 'to', 'recipients']
        read_only_fields = ('is_send', )


class EmailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emails
        fields = ['id', 'email']


class RecipientsSerializer(serializers.ModelSerializer):
    email = EmailsSerializer()

    class Meta:
        model = Recipients
        fields = ['id', 'email', 'message', 'item']
        read_only_fields = ('is_send',)

    def create(self, validated_data):
        email_data = validated_data.pop('email')
        email, _ = Emails.objects.get_or_create(email=email_data['email'])
        message = validated_data.pop('message')
        recipient = Recipients.objects.create(message=message, email=email, **validated_data)
        return recipient
