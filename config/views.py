from rest_framework import status, generics
from rest_framework.response import Response

from src.StaffControl.Employees.serializers import RegisterSerializer, UserSerializer

from config.camera_finder import finder


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
        """
        Returns a list of cameras available to connect
        """
        cameras = finder.fetch_devices()
        return Response({"results": cameras}, status=status.HTTP_200_OK)
