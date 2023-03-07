from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from src.OrderView.models import Skany, SkanyVsZlecenia, Zlecenia

from src.OrderView.serializers import ZleceniaSerializer


import json

from src.OrderView.services import order_service


class GetAllDataAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        results = order_service.get_data()
        serialized_results = json.dumps(results, status=status.HTTP_200_OK)
        return Response(serialized_results, content_type="application/json")


class ZlecenieList(generics.ListAPIView):
    serializer_class = ZleceniaSerializer

    def get_queryset(self):
        zlecenia = Zlecenia.objects.using("mssql").all()
        results = []
        for zlecenie in zlecenia:
            skany_zlecenia = (
                SkanyVsZlecenia.objects.using("mssql")
                .filter(indekszlecenia=zlecenie.indeks)
                .first()
            )
            if not skany_zlecenia:
                zlecenie.skany = None
            else:
                skany = (
                    Skany.objects.using("mssql")
                    .filter(indeks=skany_zlecenia.indeksskanu)
                    .first()
                )
                if not skany:
                    zlecenie.skany = None
                else:
                    zlecenie.skany = skany
            results.append(zlecenie)
        return results
