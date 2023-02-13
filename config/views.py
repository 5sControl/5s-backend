from django.http import HttpResponse
from rest_framework import generics
from rest_framework.views import APIView
from src.StaffControl.Employees.serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response
import subprocess
from netifaces import interfaces, ifaddresses, AF_INET


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


def setcookie(request):
    response = HttpResponse("Cookie Set")
    response.set_cookie("java-tutorial", "javatpoint.com")
    return response


def getcookie(request):
    tutorial = request.COOKIES["java-tutorial"]
    return HttpResponse("java tutorials @: " + tutorial)
