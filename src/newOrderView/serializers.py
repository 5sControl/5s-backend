from rest_framework import serializers


class ZleceniaSerializer(serializers.Serializer):
    from_date = serializers.DateField()
    to_date = serializers.DateField()
