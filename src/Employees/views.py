from src.Employees.models import CustomUser
from src.Core.permissions import IsSuperuserPermission, IsAdminPermission

from src.Employees.serializers import UserSerializer, CreateUserSerializer

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth.hashers import make_password

from src.erp_5s.models import ReferenceItems
from src.erp_5s.serializers import ReferenceItemsSerializerEmployees


class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission, IsAdminPermission]
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if CustomUser.objects.filter(username=serializer.validated_data["username"]).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()


class UserListApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission, IsAdminPermission]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = None


class UserInfoFromToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsSuperuserPermission, IsAdminPermission]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        password = request.data.get('password')
        if password:
            if request.user != instance and request.user.role not in [CustomUser.ADMIN, CustomUser.SUPERUSER]:
                return Response({"detail": "You cannot change another user's password."}, status=403)
            if not password.strip():
                return Response({"detail": "Password cannot be empty."}, status=400)

            instance.password = make_password(password)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()


class WorkplaceEmployees(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        items = ReferenceItems.objects.filter(reference__name="workplace")
        serializer = ReferenceItemsSerializerEmployees(items, many=True)
        return Response(serializer.data, status=200)
