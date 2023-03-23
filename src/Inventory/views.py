from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from src.Inventory.models import Items

from src.Inventory.serializers import ItemsSerializer

from src.Reports.views import ReportListView


class ItemsViewSet(ModelViewSet):
    """All items in the inventory"""
    queryset = Items.objects.all().order_by("-id")
    serializer_class = ItemsSerializer
    permission_classes = [IsAuthenticated]


class ItemsHistoryViewSet(APIView):
    """History items"""
    # permission_classes = [IsAuthenticated]

    def get(self, request, camera_ip, date, start_time, end_time):
        report_view = ReportListView()
        response = report_view.get(request, "min_max_control", camera_ip, date, start_time, end_time)
        data = response.data
        return Response(data)
