from django.contrib.auth.models import User

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

from src.Core.permissions import IsSuperuserPermission

from src.Employees.services import user_manager
from src.Employees.serializers import RegisterSerializer, UserSerializer


class CreateUserView(generics.GenericAPIView):
    """Create new staff or worker user"""

    permission_classes = [IsAuthenticated, IsSuperuserPermission]
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user_type = request.data.get("user_type")
        username = request.data.get("username")
        password = request.data.get("password")

        if not user_type or not username or not password:
            return Response({"error": "user_type, username, and password are required"})

        if user_type == "staff":
            user_manager.create_staff(username, password)
        elif user_type == "worker":
            user_manager.create_worker(username, password)
        else:
            return Response(
                data={"error": 'user_type must be "staff" or "worker"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_201_CREATED)


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
                    user,
                    context=self.get_serializer_context()
                ).data,
                "message": "User has been successfully created",
            }
        )


class UserListApiView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
