from rest_framework import viewsets
from .models import ManifestConnection
from .serializers import ManifestConnectionSerializer


class ManifestConnectionViewSet(viewsets.ModelViewSet):
    queryset = ManifestConnection.objects.all()
    serializer_class = ManifestConnectionSerializer