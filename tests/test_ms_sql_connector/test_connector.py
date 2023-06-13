from django.core.management import call_command
from django.contrib.auth.models import User
from django.test import RequestFactory

from rest_framework.test import APITestCase
from rest_framework import status


class CreateDatabaseConnectionAPIViewTestCase(APITestCase):
    fixtures = ["tests/fixtures/lic.json", "tests/fixtures/comp.json"]

    @classmethod
    def setUpTestData(cls):
        cls.load_fixtures()
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    @classmethod
    def load_fixtures(cls):
        for fixture in cls.fixtures:
            call_command("loaddata", fixture, verbosity=0)

    def test_create_valid_connection(self):
        url = "/api/order/create-connection/"
        data = {
            "database_type": "orderview",
            "server": "192.168.1.110",
            "database": "test",
            "username": "sa",
            "password": "just4Taqtile",
            "port": "1433",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(
            response.data["message"], "Database connection was created successfully"
        )

    def test_create_invalid_connection(self):
        url = "/api/order/create-connection/"
        data = {
            "database_type": "orderview",
            "server": "192.168.1.119",
            "database": "incorrect",
            "username": "incorrect",
            "password": "incorrect",
            "port": "1433",
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["success"], False)
