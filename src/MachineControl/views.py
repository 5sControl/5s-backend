from datetime import datetime, time, timedelta
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from src.MachineControl.models import MachineAction
from src.MachineControl.serializers import MachineControlSerializers
from rest_framework.permissions import IsAuthenticated


class MachineControlViewSet(ModelViewSet):
    """List of all Actions on MachineControl"""

    serializer_class = MachineControlSerializers
    queryset = MachineAction.objects.all().order_by("-id")

    # def get_permissions(self):
    #     if self.request.method != "POST":
    #         return [IsAuthenticated()]
    #     return []


class MachineActionListView(APIView):
    def get(self, request):
        today = datetime.today().date()
        start_of_day = datetime.combine(today, time.min)
        end_of_day = datetime.combine(today, time.max)

        queryset = MachineAction.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        serializer = MachineControlSerializers(queryset, many=True)
        return Response(serializer.data)
