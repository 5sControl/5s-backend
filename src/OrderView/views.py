from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer

from src.OrderView.models import Stanowiska, Zlecenia, SkanyVsZlecenia, Skany
from src.OrderView.services import order_service

from django.forms.models import model_to_dict


class GetAllDataAPIView(generics.ListAPIView):
    serializer_class = ZleceniaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return order_service.get_data()


class ZleceniaSkansAPIView(APIView):
    def get(self, request):
        zleceniaQuery = Zlecenia.objects.using("mssql").all()

        response_list = []

        for zlecenie in zleceniaQuery:
            skanyVsZleceniaQuery = SkanyVsZlecenia.objects.using("mssql").filter(
                indekszlecenia=zlecenie.indeks
            )
            skany_list = []
            for skanyVsZlecenia in skanyVsZleceniaQuery:
                skanyQuery = Skany.objects.using("mssql").filter(
                    indeks=skanyVsZlecenia.indeksskanu
                )
                for skany in skanyQuery:
                    stanowisko = Stanowiska.objects.using("mssql").get(id=skany.stanowisko_id)
                    skany_data = model_to_dict(skany)
                    skany_data["raport"] = stanowisko.raport
                    skany_list.append(skany_data)

            zlecenie_data = model_to_dict(zlecenie)
            zlecenie_data["skans"] = skany_list
            response_list.append(zlecenie_data)

        return Response(response_list, status=status.HTTP_200_OK)

