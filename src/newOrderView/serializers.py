from rest_framework import serializers

from .models import FiltrationOperationsTypeID


class FilterOperationsTypeIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = FiltrationOperationsTypeID
        fields = "__all__"
