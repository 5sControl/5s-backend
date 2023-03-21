from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from src.Inventory.models import Items

from src.Inventory.serializers import ItemsSerializer


class ItemsViewSet(ModelViewSet):
    queryset = Items.objects.all().order_by("-id")
    serializer_class = ItemsSerializer
    # permission_classes = [IsAuthenticated]
