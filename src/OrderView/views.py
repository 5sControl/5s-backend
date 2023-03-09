from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from src.OrderView.serializers import ZleceniaSerializer, ZleceniaTestSerializer

from src.OrderView.models import Zlecenia, SkanyVsZlecenia
from src.OrderView.services import order_service

from django.db.models import F
from django.db import connection


class GetAllDataAPIView(generics.ListAPIView):
    serializer_class = ZleceniaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return order_service.get_data()


class ZleceniaListView(generics.ListAPIView):
    serializer_class = ZleceniaTestSerializer

    def get_queryset(self):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT Z.*, S.Raport
                FROM Zlecenia Z
                JOIN SkanyVsZlecenia SZ ON Z.indeks = SZ.indekszlecenia
                JOIN Skany S ON SZ.indeksskanu = S.indeks
                WHERE NOT EXISTS (
                    SELECT *
                    FROM SkanyVsZlecenia SZ2
                    WHERE SZ2.indekszlecenia = Z.indeks
                    AND SZ2.indeksskanu NOT IN (
                        SELECT S2.indeks
                        FROM Skany S2
                        WHERE S2.Stanowisko IN (
                            SELECT Stanowisko
                            FROM Skany
                            WHERE indeks = S.indeks
                        ) AND S2.indeks = SZ2.indeksskanu
                    )
                )
                AND S.Stanowisko IN (
                    SELECT Stanowisko
                    FROM Skany
                    WHERE indeks = S.indeks
                ) AND S.Raport IS NOT NULL
            """)

            rows = cursor.fetchall()
            queryset = []
            for row in rows:
                zlecenie = Zlecenia(*row[:-1])
                zlecenie.raport = row[-1]
                queryset.append(zlecenie)

        return queryset
    
