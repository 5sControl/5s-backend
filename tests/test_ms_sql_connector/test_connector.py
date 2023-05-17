from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from src.OrderView.views import CreateDatabaseConnectionAPIView
from ..create_force_user import create_user


class CreateDatabaseConnectionAPIViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user(username='testuser', password='testpassword')

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
        force_authenticate(request, user=self.user)

        view = CreateDatabaseConnectionAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Database connection was created successfully")

    def test_create_invalid_connection(self):
        url = '/path/to/create/'
        data = {
            "database_type": "orderview",
            "server": "192.168.1.110",
            "database": "error",
            "username": "error",
            "password": "error",
            "port": "1433"
        }
        request = self.factory.post(url, data)
        force_authenticate(request, user=self.user)

        view = CreateDatabaseConnectionAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["message"], "Database connection was not created successfully")
