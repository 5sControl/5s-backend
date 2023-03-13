from src.OrderView.models import Stanowiska, Uzytkownicy, Zlecenia, SkanyVsZlecenia, Skany

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
            .values("indeks", "data", "stanowisko", "uzytkownik")
        )

    def get_zleceniaDictByIndeks(self, id):
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
        zlecenia_dict = (
            Zlecenia.objects.using("mssql")
            .annotate(
                orderName=Value("Order Name", output_field=CharField()),
                status=Case(
                    When(
                        zakonczone=0, datawejscia__isnull=False, then=Value("Started")
                    ),
                    default=Value("Completed"),
                    output_field=CharField(),
                )            )
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
                "terminrealizacji",
                "status",
            )
        )
        return zlecenia_dict

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
        zlecenie_data = orderView_service.get_zleceniaDictByIndeks(order_id)

        response_list = []

        for zlecenie in zlecenie_data:
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

        response = {}
        status = "Completed"

        zlecenia_dict = orderView_service.get_zleceniaQueryByZlecenie(zlecenie)

        for zlecenie_obj in zlecenia_dict:
            if zlecenie_obj["status"] == "Started":
                status = "Started"
                break
            skanyVsZleceniaQuery = SkanyVsZlecenia.objects.using("mssql").filter(
                indekszlecenia=zlecenie_obj["indeks"]
            )
            skany_list = []
            for skanyVsZlecenia in skanyVsZleceniaQuery:
                skanyQuery = orderView_service.get_skanyQueryById(
                    skanyVsZlecenia.indeksskanu
                )

                for skany in skanyQuery:
                    stanowisko = Stanowiska.objects.using("mssql").filter(
                        indeks=skany["stanowisko"]
                    ).first()
                    uzytkownik = Uzytkownicy.objects.using("mssql").filter(
                        indeks=skany["uzytkownik"]
                    ).first()
                    skany["worker"] = uzytkownik.imie
                    skany["raport"] = stanowisko.raport
                    skany_list.append(skany)

            zlecenie_obj["skans"] = skany_list

        response["products"] = list(zlecenia_dict)

        response["status"] = status
        response["data"] = response["products"]["data"]
        response["klient"] = response["products"]["klient"]
        response["datawejscia"] = response["products"]["datawejscia"]
        response["terminrealizacji"] = response["products"]["terminrealizacji"]

        return [response]


orderView_service = OrderService()
