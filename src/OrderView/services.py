from src.OrderView.models import Stanowiska, Zlecenia, SkanyVsZlecenia, Skany

from django.db import models
from django.forms.models import model_to_dict
from django.db.models import Case, When, Value, CharField, Subquery, OuterRef


class OrderService:
    def get_zleceniaQuery(
        self,
    ):
        return Zlecenia.objects.using("mssql").all()

    def get_skanyQueryById(self, id):
        return (
            Skany.objects.using("mssql")
            .filter(indeks=id)
            .values("indeks", "data", "stanowisko")
        )

    def get_zleceniaQueryByIndeks(self, id):
        return (
            Zlecenia.objects.using("mssql")
            .annotate(orderName=Value("Order Name", output_field=models.CharField()))  # FIXME
            .filter(indeks=id)
            .values(
                "indeks",
                "data",
                "zlecenie",
                "klient",
                "datawejscia",
                "terminrealizacji",
                "zakonczone",
                "typ",
                "orderName",
            )
        )

    def get_zlecenia_query_by_zlecenie(self, zlecenie):    
        zlecenia_query = Zlecenia.objects.using("mssql")
        
        # Add annotations to the query
        zlecenia_query = zlecenia_query.annotate(
            orderName=Value("Order Name", output_field=CharField()),
            status=Case(
                When(
                    zakonczone=0, datawejscia__isnull=False, then=Value("Started")
                ),
                default=Value("Completed"),
                output_field=CharField()
            ),
            worker=Value("Zubenko Mihail Petrovich", output_field=CharField()),
        )
        
        # Filter the query based on the given zlecenie parameter
        zlecenia_query = zlecenia_query.filter(zlecenie=zlecenie)
        
        # Get the indeks values from the filtered query
        indeks_list = list(zlecenia_query.values_list("indeks", flat=True))
        
        # Query the SkanyVsZlecenia table to get the corresponding indeksskanu values
        skany_indeks_list = SkanyVsZlecenia.objects.using("mssql").filter(indekszlecenia__in=indeks_list).values_list("indeksskanu", flat=True)
        
        for skany_query in skany_indeks_list:
            orderView_service.get_skanyQueryById(list(skany_query))
            
            # Query the Stanowiska table for each row in the skany_query result set
            skany_list = []
            for skany in skany_query:
                stanowisko = Stanowiska.objects.using("mssql").get(indeks=skany["stanowisko"])
                skany["raport"] = stanowisko.raport
                skany_list.append(skany)
            
            # Join the Zlecenia query with the Skany data
            zlecenia_query = zlecenia_query.annotate(skany_count=Value(len(skany_list)))
            
            # Combine the Zlecenia and Skany data and return the result set
            result_list = []
            for zlecenie in zlecenia_query:
                zlecenie_dict = model_to_dict(zlecenie)
                zlecenie_dict["skany"] = [skany for skany in skany_list if skany["indeksskanu"] == zlecenie_dict["indeks"]]
                result_list.append(zlecenie_dict)
        
        return result_list



    def get_all(self):
        response = []

        zleceniaQuery = orderView_service.get_zleceniaQuery()

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
                    stanowisko = Stanowiska.objects.using("mssql").get(
                        indeks=skany.stanowisko
                    )
                    skany_data = model_to_dict(skany)
                    skany_data["raport"] = stanowisko.raport
                    skany_list.append(skany_data)

            zlecenie_data = model_to_dict(zlecenie)
            zlecenie_data["skans"] = skany_list
            zlecenie_data["orderName"] = "Order Name"  # FIXME
            response.append(zlecenie_data)

        return response

    def get_allProduct(self):
        products = (
            Zlecenia.objects.using("mssql")
            .annotate(
                status=Case(
                    When(
                        zakonczone="0", datawejscia__isnull=False, then=Value("Started")
                    ),
                    When(zakonczone="1", then=Value("Completed")),
                    default=Value("Unknown"),
                    output_field=CharField(),
                )
            )
            .values("indeks", "zlecenie", "status", "terminrealizacji")
            .distinct()
        )

        return list(products)

    def get_productDataById(self, order_id):
        zleceniaQuery = orderView_service.get_zleceniaQueryByIndeks(order_id)

        response_list = []

        for zlecenie in zleceniaQuery:
            skanyVsZleceniaQuery = SkanyVsZlecenia.objects.using("mssql").filter(
                indekszlecenia=zlecenie["indeks"]
            )
            skany_list = []
            for skanyVsZlecenia in skanyVsZleceniaQuery:
                skanyQuery = orderView_service.get_skanyQueryById(
                    skanyVsZlecenia.indeksskanu
                )

                for skany in skanyQuery:
                    stanowisko = Stanowiska.objects.using("mssql").get(
                        indeks=skany["stanowisko"]
                    )
                    skany["raport"] = stanowisko.raport
                    skany_list.append(skany)

            zlecenie["skans"] = skany_list
            response_list.append(zlecenie)

        return response_list

    def get_order(self, zlecenie):
        response = []
        zlecenie_dict = {}

        zlecenie_data = orderView_service.get_zlecenia_query_by_zlecenie(zlecenie)
        zlecenie_dict[zlecenie] = list(zlecenie_data)

        status = "Completed"

        for zlecenie_item in zlecenie_data:
            if zlecenie_item["status"] == "Started":
                status = "Started"
                break

        zlecenie_dict["status"] = status
        response.append(zlecenie_dict)

        return response


orderView_service = OrderService()
