from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from src.Suppliers.models import Suppliers
from src.Suppliers.serializers import SuppliersSerializer


class SuppliersView(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = Suppliers.objects.all().order_by('id')
    serializer_class = SuppliersSerializer
