from rest_framework import serializers
from .models import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = ["id", "image", "action", "name_file", "camera", "date_created"]
