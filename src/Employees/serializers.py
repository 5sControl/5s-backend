from rest_framework import serializers

from src.Employees.models import CustomUser
from src.erp_5s.models import ReferenceItems
from src.erp_5s.serializers import ReferenceItemsSerializerEmployees


class UserSerializer(serializers.ModelSerializer):
    workplace = serializers.SerializerMethodField()
    workplace_id = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceItems.objects.filter(reference__name="workplace"),
        write_only=True,
        required=False
    )
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "first_name", "last_name", "date_joined", "role", "workplace", "workplace_id"]
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
        if workplace:
            instance.workplace_id = workplace.id

        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    workplace = serializers.PrimaryKeyRelatedField(
        queryset=ReferenceItems.objects.filter(reference__name="workplace"), write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'workplace']

    def create(self, validated_data):
        password = validated_data.pop('password')
        workplace = validated_data.pop('workplace', None)
        user = CustomUser(**validated_data)
        if workplace:
            user.workplace_id = workplace.id
        user.set_password(password)
        user.save()
        return user
