# manifest_api/serializers.py
from rest_framework import serializers
from .models import ManifestConnection


class ManifestConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManifestConnection
        fields = ('host', 'username', 'password')
