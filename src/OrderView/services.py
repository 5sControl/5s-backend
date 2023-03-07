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
                print(zlecenie.indeks)
                zlecenie_dict = zlecenie.__dict__
                del zlecenie_dict['_state']
                zlecenie_dict['skany'] = None
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
                del zlecenie_dict['_state']
                zlecenie_dict['skany'] = None
                final_data = zlecenie_dict
                results.append(final_data)
                continue
            skany_dict = skany.__dict__
            zlecenie_dict = zlecenie.__dict__
            del skany_dict['_state']
            del zlecenie_dict['_state']
            zlecenie_dict['skany'] = skany_dict
            final_data = zlecenie_dict
            results.append(final_data)
    
        return results


order_service = OrderService()
