from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.ReportsAI.models import ExtensionReport
from src.ReportsAI.serializers import ExtensionReportSerializer


class ExtensionReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = ExtensionReport.objects.all()
    serializer_class = ExtensionReportSerializer
