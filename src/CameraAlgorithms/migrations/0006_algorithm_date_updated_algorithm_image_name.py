# Generated by Django 4.2.1 on 2023-09-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CameraAlgorithms", "0005_alter_zonecameras_camera"),
    ]

    operations = [
        migrations.AddField(
            model_name="algorithm",
            name="date_updated",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="algorithm",
            name="image_name",
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
