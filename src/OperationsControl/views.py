from datetime import datetime, time
from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from src.OperationsControl.models import OperationsCounter
from src.OperationsControl.serializers import OperationControlSerializers
from rest_framework.permissions import IsAuthenticated


class OperationsControlViewSet(APIView):
    """All of operations """
    def get(self, request):
        queryset = OperationsCounter.objects.all()
        serializer_for_queryset = OperationControlSerializers(
            instance=queryset,
            many=True
        )
        data = {
            "date_counter": len(serializer_for_queryset.data),
            "list_all_date": serializer_for_queryset.data
        }
        return Response(data)

    def post(self, request):
        article = request.data
        serializer = OperationControlSerializers(data=article)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"message": "Data successfully"}, status=status.HTTP_201_CREATED)

    def get_permissions(self):
        if self.request.method != "POST":
            return [IsAuthenticated()]
        return []


class OperationsListView(APIView):
    permission_classes = [IsAuthenticated]

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
