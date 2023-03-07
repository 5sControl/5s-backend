from src.OrderView.models import Skany
from src.OrderView.models import Zlecenia, SkanyVsZlecenia, Skany


class OrderService:
    def get_data(self):
        zlecenia = Zlecenia.objects.using("mssql").all()
        results = []
        for zlecenie in zlecenia:
            skany_zlecenia = (
                SkanyVsZlecenia.objects.using("mssql")
                .filter(indekszlecenia=zlecenie.indeks)
                .first()
            )
            if not skany_zlecenia:
                result = {"zlecenie": zlecenie, "skany": None}
                continue
            skany = (
                Skany.objects.using("mssql")
                .filter(indeks=skany_zlecenia.indeksskanu)
                .first()
            )
            result = {"zlecenie": zlecenie, "skany": skany}
            results.append(result)


order_service = OrderService()
