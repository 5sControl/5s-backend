# Generated by Django 4.2.1 on 2023-06-08 06:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Reports", "0004_alter_skanyreport_operation_time"),
    ]

    operations = [
        migrations.RenameField(
            model_name="skanyreport",
            old_name="operation_time",
            new_name="end_time",
        ),
        migrations.AddField(
            model_name="skanyreport",
            name="start_time",
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]