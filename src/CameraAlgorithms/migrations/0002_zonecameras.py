# Generated by Django 4.2.1 on 2023-06-05 10:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("CameraAlgorithms", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ZoneCameras",
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
                ("coords", models.JSONField(verbose_name="Zone coordinates")),
                ("name", models.CharField(blank=True, max_length=100, null=True)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "date_created",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date created"
                    ),
                ),
                (
                    "date_updated",
                    models.DateTimeField(auto_now=True, verbose_name="Date updated"),
                ),
                (
                    "camera",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="Zone_cameras",
                        to="CameraAlgorithms.camera",
                    ),
                ),
            ],
        ),
    ]
