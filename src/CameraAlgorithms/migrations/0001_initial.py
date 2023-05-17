# Generated by Django 4.1.4 on 2023-05-16 07:23

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Algorithm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("is_available", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            options={
                "verbose_name": "Algorithm",
                "verbose_name_plural": "Algorithms",
                "db_table": "algorithm",
            },
        ),
        migrations.CreateModel(
            name="Camera",
            fields=[
                (
                    "id",
                    models.CharField(
                        max_length=30,
                        primary_key=True,
                        serialize=False,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="ID must be a valid IP address",
                                regex="^\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}$",
                            )
                        ],
                    ),
                ),
                ("username", models.CharField(max_length=100)),
                ("password", models.CharField(max_length=250)),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "Camera",
                "verbose_name_plural": "Cameras",
                "db_table": "camera",
            },
        ),
        migrations.CreateModel(
            name="CameraAlgorithmLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("algorithm_name", models.CharField(max_length=150)),
                ("camera_ip", models.CharField(max_length=150)),
                ("stoped_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("status", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name": "CameraAlgorithmLog",
                "verbose_name_plural": "CameraAlgorithmLogs",
                "db_table": "cameraalgorithmslog",
            },
        ),
        migrations.CreateModel(
            name="CameraAlgorithm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("process_id", models.PositiveBigIntegerField(default=0)),
                (
                    "algorithm",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="CameraAlgorithms.algorithm",
                    ),
                ),
                (
                    "camera",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="CameraAlgorithms.camera",
                    ),
                ),
            ],
            options={
                "verbose_name": "CameraAlgorithm",
                "verbose_name_plural": "CameraAlgorithms",
                "db_table": "cameraalgorithm",
            },
        ),
    ]