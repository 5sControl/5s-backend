# Generated by Django 4.2.1 on 2024-02-15 06:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CameraAlgorithms", "0009_algorithm_date_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithm",
            name="used_in",
            field=models.CharField(
                choices=[
                    ("dashboard", "Dashboard"),
                    ("orders_view", "Orders View"),
                    ("inventory", "Inventory"),
                ],
                default="dashboard",
                max_length=20,
            ),
        ),
    ]
