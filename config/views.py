from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from apps.Employees.serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
import os


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


class GetIp(APIView):
    """Get Ip address of local machine."""

    def get(self, request, *args, **kwargs):
        host_ip = os.environ.get("HOST_IP")
        camera_url = os.environ.get("CAMERA_URL")
        return Response({"host_ip": host_ip, "camera_url": camera_url})


def setcookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie("java-tutorial", "javatpoint.com")
    return response


def getcookie(request):
    tutorial = request.COOKIES["java-tutorial"]
    return HttpResponse("java tutorials @: " + tutorial)
