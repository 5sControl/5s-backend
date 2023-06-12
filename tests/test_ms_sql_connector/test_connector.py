import inspect

from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.core.management import call_command

from rest_framework import status
from rest_framework.test import force_authenticate

from src.OrderView.views import CreateDatabaseConnectionAPIView


class CreateDatabaseConnectionAPIViewTestCase(TestCase):
    fixtures = ['tests/fixtures/lic.json', 'tests/fixtures/comp.json']

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

    def test_create_valid_connection(self):
        url = '/api/order/create-connection/'
        data = {
            "database_type": "orderview",
            "server": "192.168.1.110",
            "database": "test",
            "username": "sa",
            "password": "just4Taqtile",
            "port": "1433"
        }
        request = self.factory.post(url, data)
        request.content_type = 'application/json'
        force_authenticate(request, user=self.user)

        view = CreateDatabaseConnectionAPIView.as_view()
        response = view(request)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Database connection was created successfully")

        print(1)

    def test_create_invalid_connection(self):
        url = '/api/order/create-connection/'
        data = {
            "database_type": "orderview",
            "server": "192.168.1.119",
            "database": "incorrect",
            "username": "incorrect",
            "password": "incorrect",
            "port": "1433"
        }
        request = self.factory.post(url, data)
        request.content_type = 'application/json'
        force_authenticate(request, user=self.user)

        view = CreateDatabaseConnectionAPIView.as_view()
        response = view(request)

        data = response.data

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(data["success"], False)

        print(2)