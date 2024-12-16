from rest_framework import serializers
from django.contrib.auth.models import User

from src.erp_5s.models import References, ReferenceItems, Operations, Items, Orders, OrderItems, OrderOperations, \
    OrderOperationDynamicInfo, OrderOperationTimespan


class ReferenceItemsSerializerEmployees(serializers.ModelSerializer):

    class Meta:
        model = ReferenceItems
        fields = ["id", "name"]


class ReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = References
        fields = '__all__'


class ReferenceItemsSerializer(serializers.ModelSerializer):
    # rename field operationName -> workplace_name
    operationName = serializers.CharField(source='name')

    class Meta:
        model = ReferenceItems
        fields = ["id", "operationName"]


class OperationsSerializer(serializers.ModelSerializer):
    operationName = serializers.CharField(source='name')

    class Meta:
        model = Operations
        fields = ["id", "operationName"]


class ItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'


class OrderOperationDynamicInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOperationDynamicInfo
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class OperationsOrdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operations
        fields = ["id", "name"]


class OrderOperationTimespanSerializer(serializers.ModelSerializer):
    employee = UserSerializer()

    class Meta:
        model = OrderOperationTimespan
        fields = ['id', 'started_at', 'finished_at', 'employee']


class OrderOperationsSerializer(serializers.ModelSerializer):
    operation = OperationsOrdSerializer()
    timespans = OrderOperationTimespanSerializer(source='orderoperationtimespan_set', many=True)
    order_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderOperations
        fields = ['id', 'operation', 'order_id', 'order_name', 'timespans']

    def get_order_name(self, obj):
        try:
            order = Orders.objects.get(id=obj.order_id)
            return order.name
        except Orders.DoesNotExist:
            return None


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ["id", "name"]


class OrderItemsSerializer(serializers.ModelSerializer):
    operations = OrderOperationsSerializer(source='orderoperations_set', many=True)
    item = ItemSerializer()

    class Meta:
        model = OrderItems
        fields = ['id', 'item', 'operations']


class OrdersSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(source='orderitems_set', many=True)

    class Meta:
        model = Orders
        fields = ['id', 'order_number', 'name', 'status', 'order_items']
