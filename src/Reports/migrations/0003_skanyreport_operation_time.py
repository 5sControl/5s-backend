# Generated by Django 4.2.1 on 2023-06-06 10:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Reports", "0002_alter_report_camera"),
    ]

    operations = [
        migrations.AddField(
            model_name="skanyreport",
            name="operation_time",
            field=models.FloatField(blank=True, null=True),
        ),
    ]