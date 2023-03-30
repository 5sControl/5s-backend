from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from src.Inventory.models import Items

from src.Inventory.serializers import ItemsSerializer

from src.Reports.views import ReportListView


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context and 'response' in renderer_context:
            response = renderer_context['response']
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return super().render({"message": "Item deleted successfully."}, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)


class ItemsViewSet(ModelViewSet):
    """All items in the inventory"""
    queryset = Items.objects.all().order_by("-id")
    serializer_class = ItemsSerializer
    renderer_classes = [CustomJSONRenderer]
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemsHistoryViewSet(APIView):
    """History items"""

    permission_classes = [IsAuthenticated]

    def get(self, request, camera_ip, date, start_time, end_time):
        report_view = ReportListView()
        response = report_view.get(request, "min_max_control", camera_ip, date, start_time, end_time)
        data = response.data
        return Response(data)
