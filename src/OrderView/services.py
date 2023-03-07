from datetime import datetime
import json

from django.http import JsonResponse

from src.OrderView.models import Zlecenia, SkanyVsZlecenia, Skany
from src.OrderView.serializers import ZleceniaSerializer


class OrderService:
    def test_get_data(request):
        zlecenia = Zlecenia.objects.using("mssql").all()
        serialized_data = ZleceniaSerializer(zlecenia, many=True)
        return JsonResponse(serialized_data.data, safe=False)

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
                print(zlecenie.indeks)
                zlecenie_dict = zlecenie.__dict__
                del zlecenie_dict["_state"]
                zlecenie_dict["skany"] = None
                final_data = zlecenie_dict
                results.append(final_data)
                continue
            skany = (
                Skany.objects.using("mssql")
                .filter(indeks=skany_zlecenia.indeksskanu)
                .first()
            )
            if not skany:
                print(zlecenie.indeks)
                zlecenie_dict = zlecenie.__dict__
                del zlecenie_dict["_state"]
                zlecenie_dict["skany"] = None
                final_data = zlecenie_dict
                results.append(final_data)
                continue
            skany_dict = skany.__dict__
            zlecenie_dict = zlecenie.__dict__
            del skany_dict["_state"]
            del zlecenie_dict["_state"]
            zlecenie_dict["skany"] = skany_dict

            # Convert datetime objects to strings
            for key, value in zlecenie_dict.items():
                if isinstance(value, datetime):
                    zlecenie_dict[key] = str(value)

            final_data = zlecenie_dict
            results.append(final_data)

        # Serialize the results to JSON
        return json.dumps(results)

    def datetime_to_str(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S.%f")
        else:
            return str(obj)


order_service = OrderService()
