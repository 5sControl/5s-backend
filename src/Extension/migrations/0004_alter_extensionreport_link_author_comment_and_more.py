# Generated by Django 4.2.1 on 2024-01-26 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Extension", "0003_alter_extensionreport_link_author_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="extensionreport",
            name="link_author_comment",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="extensionreport",
            name="user_link",
            field=models.TextField(blank=True, null=True),
        ),
    ]