from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from src.Core.permissions import IsSuperuserPermission

from src.Employees.services import user_manager
from src.Employees.serializers import UserSerializer


class CreateUserView(generics.GenericAPIView):
    """Create new staff or worker user"""

    permission_classes = [IsAuthenticated, IsSuperuserPermission]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_type = request.data.get("user_type")
        username = request.data.get("username")
        password = request.data.get("password")

        if not user_type or not username or not password:
            return Response(
                data={"error": "user_type, username, and password are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not User.objects.filter(username=username).exists():
            if user_type.lower() == "admin":
                user_manager.create_admin(username, password)
            elif user_type.lower() == "worker":
                user_manager.create_worker(username, password)
            else:
                return Response(
                    data={"error": 'user_type must be "admin" or "worker"'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"error": 'user exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)


class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
