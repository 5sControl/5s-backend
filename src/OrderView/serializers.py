from rest_framework import serializers
from .models import Zlecenia, Skany


class SkanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Skany
        fields = "__all__"


class ZleceniaSerializer(serializers.ModelSerializer):
    skany = SkanySerializer(many=True, read_only=True)

    class Meta:
        model = Zlecenia
        fields = "__all__"
