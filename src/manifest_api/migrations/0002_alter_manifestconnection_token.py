# Generated by Django 4.2.1 on 2024-07-12 07:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manifest_api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manifestconnection",
            name="token",
            field=models.CharField(blank=True, max_length=500),
        ),
    ]