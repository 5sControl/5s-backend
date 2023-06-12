from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate
from django.core.management import call_command
from src.OrderView.views import CreateDatabaseConnectionAPIView


class CreateDatabaseConnectionAPIViewTestCase(TestCase):
    fixtures = ['tests/fixtures/lic.json', 'tests/fixtures/comp.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.load_fixtures()
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

    @classmethod
    def load_fixtures(cls):
        for fixture in cls.fixtures:
            call_command('loaddata', fixture, verbosity=0)

    def test_create_valid_connection(self):
        url = '/api/new-order/operations/?from=2023-02-28&to=2023-02-28'

        request = self.factory.get(url)
        request.content_type = 'application/json'
        force_authenticate(request, user=self.user)

        view = CreateDatabaseConnectionAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], True)
        self.assertEqual(response.data["message"], "Database connection was created successfully")
