from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer
from src.OrderView.models import Zlecenia


class ZleceniaList(generics.ListAPIView):
    queryset = Zlecenia.objects.using('mssql').all()
    serializer_class = ZleceniaSerializer

