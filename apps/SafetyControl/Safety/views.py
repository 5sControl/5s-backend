from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from apps.SafetyControl.Safety.models import Action
from apps.SafetyControl.Safety.serializers import ActionSerializer


class ActionViewSet(ModelViewSet):
    """List of all action"""

    serializer_class = ActionSerializer
    queryset = Action.objects.all().order_by("-id")

    def get_permissions(self):
        if self.request.method != "POST":
            return [IsAuthenticated()]
        return []
