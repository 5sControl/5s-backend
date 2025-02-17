import smtplib
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now

from email.message import EmailMessage

from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError


from src.Employees.models import CustomUser, PasswordResetCode
from src.Employees.serializers import UserSerializer, CreateUserSerializer, PasswordResetRequestSerializer, \
    SetNewPasswordSerializer, VerifyResetCodeSerializer
from src.Core.permissions import IsAdminOrSuperuserPermission

from src.Mailer.models import SMTPSettings
from src.Mailer.service import text_message_reset_password
from src.erp_5s.models import ReferenceItems
from src.erp_5s.serializers import ReferenceItemsSerializerEmployees


class CreateUserView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperuserPermission]
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
    permission_classes = [IsAuthenticated, IsAdminOrSuperuserPermission]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    pagination_class = None


class UserInfoFromToken(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSuperuserPermission]
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

        if 'workplace_id' in request.data:
            workplace_id = request.data.get('workplace_id')
            print(workplace_id)
            if workplace_id is None:
                instance.workplace_id = None
            else:
                if not ReferenceItems.objects.filter(id=workplace_id).exists():
                    raise ValidationError({"workplace_id": "Workplace with this ID does not exist."})

            instance.workplace_id = workplace_id

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


class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"{request.build_absolute_uri('/api/employees/password-reset/confirm/')}{uid}/{token}/"

            # Email content
            subject = "Password Reset Request"
            message = f"Use the following link to reset your password:\n\n{reset_link}\n\n" \
                      f"If you did not request this, please ignore this email."

            try:
                smtp_settings = SMTPSettings.objects.first()
                if not smtp_settings:
                    return Response({"error": "Email service is not configured."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                with smtplib.SMTP_SSL(smtp_settings.server, smtp_settings.port) as smtp:
                    smtp.login(smtp_settings.username, smtp_settings.password)

                    email_message = EmailMessage()
                    email_message['Subject'] = subject
                    email_message['From'] = smtp_settings.username
                    email_message['To'] = email
                    email_message.set_content(message)

                    smtp.send_message(email_message)

                return Response({"message": "The link for resetting the password is sent to your mail."},
                                 status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": "Failed to send email. Please try again later."},
                                 status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendPasswordResetCodeView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            language_code = serializer.validated_data.get('language_code', 'en')
            user = CustomUser.objects.get(email=email)
            reset_code = PasswordResetCode.objects.create(user=user)
            print(reset_code.code, language_code)
            try:
                smtp_settings = SMTPSettings.objects.first()
                if not smtp_settings:
                    return Response({"error": "Email service is not configured."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                subject = "Password Reset Code"
                message = text_message_reset_password(reset_code.code, language_code)

                with smtplib.SMTP_SSL(smtp_settings.server, smtp_settings.port) as smtp:
                    smtp.login(smtp_settings.username, smtp_settings.password)

                    email_message = EmailMessage()
                    email_message['Subject'] = subject
                    email_message['From'] = smtp_settings.username
                    email_message['To'] = email
                    email_message.set_content(message)

                    smtp.send_message(email_message)

                return Response({"message": "The code for resetting the password is sent to your email."},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": "Failed to send email. Please try again later."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetCodeView(APIView):
    def post(self, request):
        serializer = VerifyResetCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                reset_code = PasswordResetCode.objects.get(user__email=email, code=code)
            except PasswordResetCode.DoesNotExist:
                return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

            if reset_code.expires_at < now():
                return Response({"error": "Code has expired"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Code is valid"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordView(APIView):
    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            new_password = serializer.validated_data['new_password']

            try:
                reset_code = PasswordResetCode.objects.get(user__email=email, code=code)
            except PasswordResetCode.DoesNotExist:
                return Response({"error": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)

            if reset_code.expires_at < now():
                return Response({"error": "Code has expired"}, status=status.HTTP_400_BAD_REQUEST)

            user = reset_code.user
            user.password = make_password(new_password)
            user.save()

            reset_code.delete()

            return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)