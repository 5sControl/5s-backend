from rest_framework import serializers

from src.Employees.models import CustomUser
from src.erp_5s.models import ReferenceItems
from src.erp_5s.serializers import ReferenceItemsSerializerEmployees


class UserSerializer(serializers.ModelSerializer):
    workplace = serializers.SerializerMethodField()
    workplace_id = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceItems.objects.filter(reference__name="workplace"),
        write_only=True,
        required=False,
        allow_null=True
    )
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "password", "first_name", "last_name", "date_joined", "role", "workplace", "workplace_id"]
        read_only_fields = ["date_joined"]

    def get_workplace(self, obj):
        if obj.workplace_id:
            try:
                workplace = ReferenceItems.objects.get(id=obj.workplace_id)
                return ReferenceItemsSerializerEmployees(workplace).data
            except ReferenceItems.DoesNotExist:
                return None
        return None

    def update(self, instance, validated_data):
        workplace = validated_data.pop("workplace_id", None)
        instance.workplace_id = workplace.id if workplace else None

        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    workplace = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceItems.objects.filter(reference__name="workplace"),
        write_only=True,
        required=False,
        allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'role', 'workplace']

    def create(self, validated_data):
        password = validated_data.pop('password')
        workplace = validated_data.pop('workplace', None)
        user = CustomUser(**validated_data)
        if workplace:
            user.workplace_id = workplace.id
        user.set_password(password)
        user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with such an email was not found.")
        return value


class VerifyResetCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data
