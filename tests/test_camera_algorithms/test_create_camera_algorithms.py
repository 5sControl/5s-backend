from django.test import TestCase, RequestFactory
from rest_framework import status
from rest_framework.test import force_authenticate

from src.CameraAlgorithms.views import CreateCameraAlgorithmsApiView, CameraAPIView
from ..create_force_user import create_user


class CreateCameraAlgorithmsApiViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user(username='testuser', password='testpassword')

    def test_create_correct_camera_only(self):
        url = '/api/camera-algorithms/create-process/'

        for i in range(1, 4):
            data = {
                "camera": {
                    "ip": f"192.168.1.{164 + i}",
                    "name": "camera",
                    "username": "admin",
                    "password": "just4Taqtile"
                },
                "algorithms": []
            }
            request = self.factory.post(url, data, content_type='application/json')
            force_authenticate(request, user=self.user)

            view = CreateCameraAlgorithmsApiView.as_view()
            response = view(request)

            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_cameras(self):
        self.test_create_correct_camera_only()

        created_camera = [f"192.168.1.{164 + i}" for i in range(1, 4)]
        url = '/api/camera-algorithms/camera/'

        request = self.factory.get(url)
        force_authenticate(request, user=self.user)

        view = CameraAPIView.as_view()
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['id'], created_camera[0])
        self.assertEqual(response.data[1]['id'], created_camera[1])
        self.assertEqual(response.data[2]['id'], created_camera[2])
