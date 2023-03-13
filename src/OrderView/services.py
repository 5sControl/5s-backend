from src.OrderView.models import Stanowiska, Zlecenia, SkanyVsZlecenia, Skany

from django.forms.models import model_to_dict
from django.db.models import Case, When, Value, CharField


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
            .annotate(orderName=Value("Order Name", output_field=CharField()))
            .filter(indeks=id)
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

    def get_zleceniaQueryByZlecenie(self, zlecenie):
        return (
            Zlecenia.objects.using("mssql")
            .annotate(orderName=Value("Order Name", output_field=CharField()))
            .filter(zlecenie=zlecenie)
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
            .values("indeks", "zlecenie", "status")
            .distinct()
        )

        return list(products)

    def get_Zlecenia(self):
        return Zlecenia.objects.using("mssql").values("zlecenie").distinct()

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

    def get_order(self):
        response = {}

        all_product_zlecenia = orderView_service.get_Zlecenia()

        for zlecenia in all_product_zlecenia:
            zlecenie_data = orderView_service.get_zleceniaQueryByZlecenie(zlecenia["zlecenie"])
            response[zlecenia["zlecenie"].strip()] = list(zlecenie_data)

        return [response]



orderView_service = OrderService()
