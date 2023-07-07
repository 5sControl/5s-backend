from rest_framework import views, response
from rest_framework.viewsets import ModelViewSet

from django_countries import countries

from src.CompanyLicense.models import Company
from src.Suppliers.serializers import SuppliersSerializer, CountrySerializer


class SuppliersView(ModelViewSet):
    pagination_class = None
    queryset = Company.objects.filter(my_company=False).order_by('id')
    serializer_class = SuppliersSerializer


class CountryListView(views.APIView):
    def get(self, request):
        country_list = []
        for code, name in countries:
            country_list.append({
                'name': name,
                'code': code
            })
        serializer = CountrySerializer(country_list, many=True)
        return response.Response(serializer.data)
