# Generated by Django 4.2.1 on 2023-09-20 05:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Inventory", "0009_remove_items_multi_row_alter_items_object_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="items",
            name="object_type",
            field=models.CharField(
                choices=[
                    ("bottle", "Bottle"),
                    ("box", "Box"),
                    ("red line", "Red Line"),
                ],
                max_length=20,
                verbose_name="Object type",
            ),
        ),
    ]
