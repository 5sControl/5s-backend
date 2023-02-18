from datetime import datetime, time
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from src.OperationsControl.models import OperationsCounter
from src.OperationsControl.serializers import OperationControlSerializers
from rest_framework.permissions import IsAuthenticated


class OperationsControlViewSet(ModelViewSet):
    serializer_class = OperationControlSerializers
    queryset = OperationsCounter.objects.all().order_by("-id")


class OperationsListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        start_of_day = datetime.combine(date_obj, time.min)
        end_of_day = datetime.combine(date_obj, time.max)

        queryset = OperationsCounter.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        serializer = OperationControlSerializers(queryset, many=True)

        data = {
           "date_counter": len(serializer.data),
            "list_all_date": serializer.data
        }

        return Response(data)
