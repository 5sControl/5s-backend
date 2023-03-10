from src.OrderView.models import Stanowiska, Zlecenia, SkanyVsZlecenia, Skany

from django.forms.models import model_to_dict
from django.db.models import Value, CharField


class OrderService:
    def get_zleceniaQuery(
        self,
    ):
        return Zlecenia.objects.using("mssql").all()

    def get_zleceniaQueryById(self, id):
        return (
            Zlecenia.objects.using("mssql")
            .annotate(orderName=Value("Order Name", output_field=CharField()))
            .filter(zlecenie=id)
            .values(
                "indeks",
                "data",
                "zlecenie",
                "klient",
                "datawejscia",
                "zakonczone",
                "typ",
                "orderName",
            )
        )

    def get_skanyQueryById(self, id):
        return (
            Skany.objects.using("mssql")
            .filter(indeks=id)
            .values("indeks", "raport", "data")
        )

    def getAllData(self):
        zleceniaQuery = orderView_service.get_zleceniaQuery()

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
                    stanowisko = Stanowiska.objects.using("mssql").get(
                        indeks=skany.stanowisko
                    )
                    skany_data = model_to_dict(skany)
                    skany_data["raport"] = stanowisko['raport']
                    skany_list.append(skany_data)

            zlecenie_data = model_to_dict(zlecenie)
            zlecenie_data["skans"] = skany_list
            zlecenie_data["orderName"] = "Order Name"  # FIXME
            response_list.append(zlecenie_data)

        return response_list

    def getAllOrders(self):
        return Zlecenia.objects.using("mssql").values_list(
            "zlecenie", flat=True
        )  # FIXME: return it when will get order name

    def getOrderDataById(self, order_id):
        zleceniaQuery = orderView_service.get_zleceniaQueryById(order_id)

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
                        indeks=skany.stanowisko
                    )
                    skany_data = model_to_dict(skany)
                    skany_data["raport"] = stanowisko.raport
                    skany_list.append(skany_data)

            zlecenie_data = zlecenie
            zlecenie_data["skans"] = skany_list
            response_list.append(zlecenie_data)

        return response_list


orderView_service = OrderService()
