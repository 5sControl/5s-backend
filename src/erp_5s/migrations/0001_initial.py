# Generated by Django 4.2.1 on 2024-11-29 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Items",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "items",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Operations",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("estimated_time", models.IntegerField(blank=True, null=True)),
                (
                    "estimated_time_unit",
                    models.CharField(default="minutes", max_length=50),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "operations",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="OrderItems",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("additional_info", models.TextField(blank=True, null=True)),
                ("quantity", models.IntegerField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "order_items",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="OrderOperationDynamicInfo",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "order_operation_dynamic_info",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="OrderOperations",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("order_id", models.IntegerField(blank=True, null=True)),
            ],
            options={
                "db_table": "order_operations",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="OrderOperationTimespan",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "order_operation_timespan",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Orders",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("status", models.CharField(default="pending", max_length=50)),
                ("started_at", models.DateTimeField(blank=True, null=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("time_taken", models.IntegerField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("order_number", models.IntegerField(blank=True, null=True)),
                ("order_year", models.IntegerField(blank=True, null=True)),
                ("estimated_at", models.DateField(blank=True, null=True)),
            ],
            options={
                "db_table": "orders",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="ReferenceItems",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": 'erp"."reference_items',
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="References",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255, unique=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "db_table": "references",
                "managed": False,
            },
        ),
    ]