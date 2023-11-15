from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from src.Core.permissions import IsSuperuserPermission

from src.Employees.services import user_manager
from src.Employees.serializers import UserSerializer, CreateUserSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_type = serializer.validated_data.get("user_type")
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")

        if not User.objects.filter(username=username).exists():
            if user_type.lower() == "admin":
                user_manager.create_admin(username, password)
            elif user_type.lower() == "worker":
                user_manager.create_worker(username, password)
            else:
                return Response(
                    data={"error": 'User Type must be "Admin" or "Worker"'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                data={"error": 'User Exists'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)


class UserListApiView(generics.ListAPIView):
    pagination_class = None
    permission_classes = [IsAuthenticated, IsSuperuserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserInfoFromToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_serializer = UserSerializer(request.user)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
