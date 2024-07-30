from rest_framework import serializers
from .models import ManifestConnection


class ManifestConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManifestConnection
        fields = ('id', 'host', 'username', 'password', 'status', 'last_updated')
        read_only_fields = ['status', 'last_updated']
