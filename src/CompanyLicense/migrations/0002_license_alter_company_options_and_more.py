# Generated by Django 4.1.4 on 2023-06-01 13:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CompanyLicense", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="License",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("license_key", models.TextField(verbose_name="Company license key")),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date joined"),
                ),
                (
                    "date_edited",
                    models.DateTimeField(auto_now=True, verbose_name="Date edited"),
                ),
                (
                    "valid_until",
                    models.DateField(verbose_name="Date which license is active"),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=False, verbose_name="Is active license"
                    ),
                ),
                (
                    "count_cameras",
                    models.IntegerField(verbose_name="Count of cameras in active"),
                ),
                (
                    "neurons_active",
                    models.IntegerField(verbose_name="Count of active neurons"),
                ),
            ],
            options={
                "verbose_name": "License",
                "verbose_name_plural": "Licenses",
            },
        ),
        migrations.AlterModelOptions(
            name="company",
            options={},
        ),
        migrations.RemoveField(
            model_name="company",
            name="count_cameras",
        ),
        migrations.RemoveField(
            model_name="company",
            name="is_active",
        ),
        migrations.RemoveField(
            model_name="company",
            name="license_key",
        ),
        migrations.RemoveField(
            model_name="company",
            name="neurons_active",
        ),
        migrations.RemoveField(
            model_name="company",
            name="valid_until",
        ),
        migrations.AddField(
            model_name="company",
            name="address_company",
            field=models.TextField(
                blank=True, null=True, verbose_name="Address of company"
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="contact_email",
            field=models.EmailField(
                blank=True, max_length=254, null=True, verbose_name="Contact email"
            ),
        ),
        migrations.AddField(
            model_name="company",
            name="contact_phone",
            field=models.TextField(
                blank=True, null=True, verbose_name="Contact phone number"
            ),
        ),
    ]