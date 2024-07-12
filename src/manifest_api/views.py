import requests

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.manifest_api.get_asset_classes import get_asset_classes
from src.manifest_api.models import ManifestConnection
from src.manifest_api.serializers import ManifestConnectionSerializer


class ManifestConnectionViewSet(viewsets.ModelViewSet):
    queryset = ManifestConnection.objects.all()
    serializer_class = ManifestConnectionSerializer


class AssetClassesView(APIView):
    def get(self, request):
        # try:
            data = get_asset_classes()
            return Response(data, status=status.HTTP_200_OK)
        # except requests.exceptions.RequestException as e:
        #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)