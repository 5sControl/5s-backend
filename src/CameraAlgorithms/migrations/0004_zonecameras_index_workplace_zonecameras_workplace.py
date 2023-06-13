# Generated by Django 4.2.1 on 2023-06-09 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CameraAlgorithms", "0003_cameraalgorithm_zones"),
    ]

    operations = [
        migrations.AddField(
            model_name="zonecameras",
            name="index_workplace",
            field=models.IntegerField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Index workplace Winkhaus",
            ),
        ),
        migrations.AddField(
            model_name="zonecameras",
            name="workplace",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="Workplace db Winkhaus",
            ),
        ),
    ]