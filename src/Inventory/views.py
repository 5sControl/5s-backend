from rest_framework.permissions import IsAuthenticated
from django.db.models import Case, When, Value, IntegerField
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework.renderers import JSONRenderer

from src.Inventory.models import Items
from src.Reports.models import Report

from django.db.models import Q
from datetime import datetime

from src.CompanyLicense.decorators import validate_license

from src.Inventory.serializers import ItemsSerializer
from src.Reports.serializers import ReportSerializers


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if renderer_context and 'response' in renderer_context:
            response = renderer_context['response']
            if response.status_code == status.HTTP_204_NO_CONTENT:
                return super().render({"message": "Item deleted successfully."}, accepted_media_type, renderer_context)
        return super().render(data, accepted_media_type, renderer_context)


class ItemsViewSet(ModelViewSet):
    """All items in the inventory"""
    queryset = Items.objects.all()
    serializer_class = ItemsSerializer
    renderer_classes = [CustomJSONRenderer]
    # permission_classes = [IsAuthenticated]

    ALLOWED_STATUSES = ["Out of stock", "Low stock level", "In stock"]

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status', None)

        # check if status is valid, else sort by default order
        if status in self.ALLOWED_STATUSES:
            queryset = queryset.order_by('status', 'id')
        else:
            queryset = queryset.order_by('id')

        return queryset

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ItemsHistoryViewSet(APIView):
    """History items"""

    # permission_classes = [IsAuthenticated]

    @validate_license
    def get(self, request, date, start_time, end_time, item_id=None):

        algorithm_name = 'min_max_control'
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

        start_of_day = datetime.combine(date_obj, start_time_obj)
        end_of_day = datetime.combine(date_obj, end_time_obj)

        queryset = Report.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by("-date_created", "-id")

        if algorithm_name:
            queryset = queryset.filter(algorithm__name=algorithm_name)

        if item_id:
            queryset = queryset.filter(extra__icontains=f'"itemId": {item_id}')

        queryset = queryset.order_by("algorithm__name", "camera__id")

        serializer = ReportSerializers(queryset, many=True)

        return Response(serializer.data)
