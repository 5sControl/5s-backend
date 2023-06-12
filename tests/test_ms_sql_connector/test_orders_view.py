import inspect

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import force_authenticate

from src.OrderView.views import GetAllProductAPIView, OperationNameApiView, GetOrderDataByZlecenieAPIView

from ..const_results import operations

class CreateDatabaseConnectionAPIViewTestCase(TestCase):
    fixtures = ['tests/fixtures/lic.json', 'tests/fixtures/comp.json', 'tests/fixtures/database_conn.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.load_fixtures()
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username='testuser', password='testpassword')
        current_test = inspect.currentframe().f_back.f_code.co_name

        print("Running test:", current_test)

    @classmethod
    def load_fixtures(cls):
        for fixture in cls.fixtures:
            call_command('loaddata', fixture, verbosity=0)

    def test_get_orders_view_orders(self):
        url = '/api/order/all-orders/'

        request = self.factory.get(url)
        request.content_type = 'application/json'
        force_authenticate(request, user=self.user)

        view = GetAllProductAPIView.as_view()
        response = view(request)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["count"] > 0, True)
        self.assertEqual(len(data["results"]) > 0, True)

    def test_get_orders_view_oprt_name(self):
        url = '/api/order/get-operations/'

        request = self.factory.get(url)
        request.content_type = 'application/json'
        force_authenticate(request, user=self.user)

        view = OperationNameApiView.as_view()
        response = view(request)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, operations)

    def test_get_list_of_all_orders_check_with_date_4(self):
        url = "/api/order/all-orders/?search=PRW199234"

        request = self.factory.get(url)
        request.content_type = 'application/json'
        force_authenticate(request, user=self.user)

        view = GetOrderDataByZlecenieAPIView.as_view()
        response = view(request)

        data = response.data

        assert response.status_code == 200

        self.assertEqual(data["count"], 1)
        self.assertEqual(data["current_page"], 1)
        self.assertEqual(data["records_on_page"], 50)
        self.assertEqual(data["all_page_count"], 1)
        self.assertEqual(len(data["results"]), 1)

        self.assertEqual(data["results"][0]["indeks"], 363992)
        self.assertEqual(data["results"][0]["zlecenie"].startswith("PRW199234"), True)
        self.assertEqual(data["results"][0]["status"], "Started")
        self.assertEqual(data["results"][0]["terminrealizacji"], "2023-03-03 00:00:00.0000000")
        self.assertEqual(data["results"][0]["datawejscia"], "23.02.2023 14:18:00")