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
    
    def get_filtered_orders_list(self):
        orders_dict = {}
        products = Zlecenia.objects.using("mssql") \
            .annotate(
                status=Case(
                    When(
                        zakonczone="0", datawejscia__isnull=False, then=Value("Started")
                    ),
                    When(zakonczone="1", then=Value("Completed")),
                    default=Value("Unknown"),
                    output_field=CharField(),
                )
            ).values("indeks", "zlecenie", "status", "terminrealizacji")

        for product in products:
            zlecenie = product["zlecenie"].strip()
            status = product["status"]

            # Keep only the first dictionary encountered for a given zlecenie value
            if zlecenie not in orders_dict:
                orders_dict[zlecenie] = product
            # If a dictionary for the same zlecenie already exists, check if its status is "Started" and replace it
            elif orders_dict[zlecenie]["status"] == "Started":
                orders_dict[zlecenie] = product

        # Return the filtered list of values
        return list(orders_dict.values())


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

        response["indeks"] = response["products"][0]["indeks"]
        response["data"] = response["products"][0]["data"]
        response["klient"] = response["products"][0]["klient"]
        response["datawejscia"] = response["products"][0]["datawejscia"]
        response["terminrealizacji"] = response["products"][0]["terminrealizacji"]

        return [response]


orderView_service = OrderService()
