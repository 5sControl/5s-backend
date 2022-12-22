
from rest_framework import generics
from apps.Employees.serializers import RegisterSerializer, UserSerializer
from rest_framework.response import Response


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,
                                   context=self.get_serializer_context()).data,
            "message": "User has been successfully created",
        })