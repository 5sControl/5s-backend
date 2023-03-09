from rest_framework import serializers
from django.http import JsonResponse

from src.OrderView.models import Zlecenia, SkanyVsZlecenia, Skany


class SkanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Skany
        fields = "__all__"


class ZleceniaSerializer(serializers.ModelSerializer):
    skany = SkanySerializer(many=False, read_only=True)

    class Meta:
        model = Zlecenia
        fields = "__all__"


class ZleceniaTestSerializer(serializers.ModelSerializer):
    skany = SkanySerializer(many=False, read_only=True)

    class Meta:
        model = Zlecenia
        fields = "__all__"
