from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from models import Items

from serializers import ItemsSerializer


class ItemsViewSet(viewsets.ModelViewSet):
    queryset = Items.objects.all().order_by("-id")
    serializer_class = ItemsSerializer
    # permission_classes = [IsAuthenticated]
