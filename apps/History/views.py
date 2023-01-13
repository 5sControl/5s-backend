from rest_framework import permissions, viewsets

from apps.base.permissions import IsAdminOrReadOnly

from .serializers import HistorySerializer
from .models import History

class HistoryViewSet(viewsets.ModelViewSet):
    """List of all history"""

    serializer_class = HistorySerializer
    queryset = History.objects.all()

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,
    # ]