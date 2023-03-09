from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer, ZleceniaTestSerializer

from src.OrderView.models import Zlecenia, SkanyVsZlecenia, Skany
from src.OrderView.services import order_service

from django.db.models import F
from django.forms.models import model_to_dict


class GetAllDataAPIView(generics.ListAPIView):
    serializer_class = ZleceniaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return order_service.get_data()


class ZleceniaSkansAPIView(APIView):
    def get(self, request):
        zleceniaQuery = Zlecenia.objects.using("mssql").all()

        zlecenia_list = []

        for zlecenie in zleceniaQuery:
            skanyVsZleceniaQuery = SkanyVsZlecenia.objects.using("mssql").filter(
                indekszlecenia=zlecenie.indeks
            )
            skany_list = []
            for skanyVsZlecenia in skanyVsZleceniaQuery:
                skanyQuery = Skany.objects.using("mssql").filter(
                    indeksskanu=skanyVsZlecenia.indeksskanu
                )
                for skany in skanyQuery:
                    skany_dict = model_to_dict(skany)
                    skany_list.append(skany_dict)

            zlecenie_dict = model_to_dict(zlecenie)
            zlecenie_dict["skans"] = skany_list
            zlecenia_list.append(zlecenie_dict)

        return Response(zlecenia_list)
