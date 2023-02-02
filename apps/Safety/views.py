from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from apps.Safety.models import Action
from apps.Safety.serializers import ActionSerializer


class ActionViewSet(ModelViewSet):
    """List of all action"""

    serializer_class = ActionSerializer
    queryset = Action.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,]
