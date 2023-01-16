from rest_framework import permissions, viewsets, generics, response, filters

from apps.base.permissions import IsAdminOrReadOnly

from .serializers import HistorySerializer
from .models import History

from django_filters import rest_framework as django_filters


class HistoryViewSet(viewsets.ModelViewSet):
    """List of all history"""

    serializer_class = HistorySerializer
    queryset = History.objects.all()

    filter_backends = [filters.SearchFilter]
    search_fields = ['action', 'location__name', 'camera__id',
            'people__first_name', 'people__last_name', 'entry_date']

    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly,
    #     IsAdminOrReadOnly,
    # ]