import requests

from rest_framework import status, generics
from rest_framework.response import Response

from config.serializers import CameraListSerializer

from src.StaffControl.Employees.serializers import RegisterSerializer, UserSerializer

from src.Algorithms.utils import yolo_proccesing


class RegisterView(generics.GenericAPIView):
    """View for registering"""

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": "User has been successfully created",
            }
        )


class FindCameraAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        cameras_response = requests.get(
            f"{yolo_proccesing.get_algorithm_url()}:7654/get_all_onvif_cameras/"
        )
        try:
            cameras = cameras_response.json()
        except ValueError as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        response_data = {"result": cameras}
        return Response(response_data, status=status.HTTP_200_OK)
