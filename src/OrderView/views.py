from rest_framework import generics
from rest_framework.views import APIView
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


class ZleceniaSkansAPIView(APIView):
    def get(self, request):
        # Query for Zlecenia objects
        zleceniaQuery = Zlecenia.objects.all()

        # Create an empty list to store skans dictionaries
        skans_list = []

        # Loop through each Zlecenia object
        for zlecenie in zleceniaQuery:
            # Query for SkanyVsZlecenia objects related to the current Zlecenia object
            skanyVsZleceniaQuery = SkanyVsZlecenia.objects.filter(indekszlecenia=zlecenie.indeks)
            # Create an empty list to store skany dictionaries for the current Zlecenia object
            skany_list = []
            # Loop through each SkanyVsZlecenia object related to the current Zlecenia object
            for skanyVsZlecenia in skanyVsZleceniaQuery:
                # Query for Skany objects related to the current SkanyVsZlecenia object
                skanyQuery = Skany.objects.filter(indeksskanu=skanyVsZlecenia.indeksskanu)
                # Loop through each Skany object related to the current SkanyVsZlecenia object
                for skany in skanyQuery:
                    # Create a dictionary for the current Skany object
                    skany_dict = {
                        'nazwa': skany.nazwa,
                        'numer': skany.numer,
                        # Add any other Skany fields you want to include in the dictionary
                    }
                    # Append the dictionary to the skany_list
                    skany_list.append(skany_dict)
            # Create a dictionary for the current Zlecenia object with the skany_list as the value for the 'skans' key
            zlecenie_dict = {
                'indeks': zlecenie.indeks,
                # Add any other Zlecenia fields you want to include in the dictionary
                'skans': skany_list,
            }
            # Append the dictionary to the skans_list
            skans_list.append(zlecenie_dict)

        # Return the skans_list in the Response object
        return Response(skans_list)







