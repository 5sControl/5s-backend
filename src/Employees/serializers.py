from rest_framework import serializers

from src.Employees.models import CustomUser
from src.erp_5s.models import ReferenceItems
from src.erp_5s.serializers import ReferenceItemsSerializerEmployees


class UserSerializer(serializers.ModelSerializer):
    workplace = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password", "first_name", "last_name", "date_joined", "role", "workplace"]
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
        password = validated_data.pop('password', None)
        if password:
            if not instance.check_password(password):
                instance.set_password(password)
                instance.save()
            return super().update(instance, validated_data)


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'first_name', 'last_name', 'role', 'workplace']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
