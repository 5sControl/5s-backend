from rest_framework import serializers
from .models import Zlecenia

class ZleceniaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zlecenia
        fields = '__all__'