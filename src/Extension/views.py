from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.Extension.models import ExtensionReport
from src.Extension.serializers import ExtensionReportSerializer


class ExtensionReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = ExtensionReport.objects.all()
    serializer_class = ExtensionReportSerializer
