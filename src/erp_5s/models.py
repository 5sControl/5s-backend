from django.db import models

from src.Employees.models import CustomUser


class References(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = '"erp"."references"'
        app_label = 'erp_5s'


class ReferenceItems(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reference = models.ForeignKey('References', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = '"erp"."reference_items"'
        app_label = 'erp_5s'


class Operations(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    estimated_time = models.IntegerField(null=True, blank=True)
    estimated_time_unit = models.CharField(max_length=50, default='minutes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = '"erp"."operations"'
        app_label = 'erp_5s'


class Items(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = '"erp"."items"'
        app_label = 'erp_5s'


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=50, default='pending')
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_number = models.IntegerField(null=True, blank=True)
    order_year = models.IntegerField(null=True, blank=True)
    estimated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    class Meta:
        managed = False
        db_table = '"erp"."orders"'
        app_label = 'erp_5s'


class OrderItems(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    additional_info = models.TextField(null=True, blank=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.ForeignKey('Orders', on_delete=models.CASCADE)
    item = models.ForeignKey('Items', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        managed = False
        db_table = '"erp"."order_items"'
        app_label = 'erp_5s'


class OrderOperations(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_id = models.IntegerField(null=True, blank=True)
    operation = models.ForeignKey('Operations', on_delete=models.CASCADE)
    order_item = models.ForeignKey('OrderItems', on_delete=models.CASCADE)

    def __str__(self):
        return f"order_operations_{self.id}"

    class Meta:
        managed = False
        db_table = '"erp"."order_operations"'
        app_label = 'erp_5s'


class OrderOperationDynamicInfo(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reference_item = models.ForeignKey('ReferenceItems', on_delete=models.CASCADE)
    order_operation = models.ForeignKey('OrderOperations', on_delete=models.CASCADE)

    def __str__(self):
        return f"order_operation_dynamic_info_{self.id}"

    class Meta:
        managed = False
        db_table = '"erp"."order_operation_dynamic_info"'
        app_label = 'erp_5s'


class OrderOperationTimespan(models.Model):
    id = models.AutoField(primary_key=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_operation = models.ForeignKey('OrderOperations', on_delete=models.CASCADE)
    employee = models.ForeignKey(CustomUser, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"order_operation_timespan_{self.id}"

    class Meta:
        managed = False
        db_table = '"erp"."order_operation_timespan"'
        app_label = 'erp_5s'
