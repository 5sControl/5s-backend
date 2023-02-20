from rest_framework.viewsets import ModelViewSet
from datetime import datetime, time
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from src.SafetyControl.models import Action
from src.SafetyControl.serializers import ActionSerializer


class ActionViewSet(ModelViewSet):
    """List of all action"""

    serializer_class = ActionSerializer
    queryset = Action.objects.all().order_by("-id")

    def get_permissions(self):
        if self.request.method != "POST":
            return [IsAuthenticated()]
        return []


class SafetyActionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        start_of_day = datetime.combine(date_obj, time.min)
        end_of_day = datetime.combine(date_obj, time.max)

        queryset = Action.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        serializer = ActionSerializer(queryset, many=True)
        return Response(serializer.data)
