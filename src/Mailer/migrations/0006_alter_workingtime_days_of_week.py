# Generated by Django 4.2.1 on 2023-11-15 06:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Mailer", "0005_alter_workingtime_days_of_week"),
    ]

    operations = [
        migrations.AlterField(
            model_name="workingtime",
            name="days_of_week",
            field=models.ManyToManyField(blank=True, to="Mailer.dayofweek"),
        ),
    ]
