from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer, ZleceniaTestSerializer

from src.OrderView.models import Zlecenia, SkanyVsZlecenia
from src.OrderView.services import order_service

from django.db.models import F


class GetAllDataAPIView(generics.ListAPIView):
    serializer_class = ZleceniaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return order_service.get_data()


class ZleceniaListView(generics.ListAPIView):
    serializer_class = ZleceniaTestSerializer

    def get_queryset(self):
        queryset = SkanyVsZlecenia.objects.filter(skanyvszlecenia__isnull=False).distinct()
        queryset = queryset.annotate(raport=F('skany__stanowisko__raport'))
        return queryset