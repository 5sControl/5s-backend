from src.OrderView.models import Skany

class OrderService:
    def get_data(self):
        Skany.objects.using('mssql').filter(indeks=1227966)


order_service = OrderService()
