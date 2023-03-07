from datetime import datetime
import json

from django.http import JsonResponse

from src.OrderView.models import Zlecenia, SkanyVsZlecenia, Skany
from src.OrderView.serializers import ZleceniaSerializer


class OrderService:
    def get_data(request):
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

order_service = OrderService()
