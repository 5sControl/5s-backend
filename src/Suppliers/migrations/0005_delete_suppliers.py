# Generated by Django 4.2.1 on 2023-06-09 13:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Inventory", "0004_alter_items_suppliers"),
        ("Suppliers", "0004_suppliers_index"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Suppliers",
        ),
    ]
