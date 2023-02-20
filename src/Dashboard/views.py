from rest_framework.views import APIView
from datetime import datetime, time
from django.db.models import Q
from rest_framework.response import Response
from src.IdleControl.models import Actions
from src.IdleControl.serializers import IdleControlSerializers
from src.MachineControl.models import MachineAction
from src.MachineControl.serializers import MachineControlSerializers
from src.SafetyControl.models import Action
from src.SafetyControl.serializers import ActionSerializer


class DashboardView(APIView):
    def get(self, request, date):

        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        start_of_day = datetime.combine(date_obj, time.min)
        end_of_day = datetime.combine(date_obj, time.max)

        machine_actions = MachineAction.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        idle_actions = Actions.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        safety_action = Action.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        machine_actions_data = MachineControlSerializers(machine_actions, many=True).data
        idle_actions_data = IdleControlSerializers(idle_actions, many=True).data
        safety_action_data = ActionSerializer(safety_action, many=True).data

        combined_data = {
            "machine_actions": machine_actions_data,
            "idle_actions": idle_actions_data,
            "safety_action": safety_action_data
        }
        return Response(combined_data)
