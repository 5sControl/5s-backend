from rest_framework import serializers


class CpuLoadSerializer(serializers.Serializer):
    cpu_load = serializers.FloatField(default=0)
