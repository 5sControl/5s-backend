from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from src.CameraAlgorithms.views import AlgorithmDetailApiView
from src.Core.management.commands.algorithm import Command
from ..create_force_user import create_user


class AlgorithmDetailApiViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Command().create_or_update_algorithms()

    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user(username='testuser', password='testpassword')

    def test_get_algorithms_details(self):
        url = '/api/camera-algorithms/algorithms-detail/'

        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        view = AlgorithmDetailApiView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 8)