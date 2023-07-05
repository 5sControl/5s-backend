from django.db import models


class DatabaseConnection(models.Model):
    DBMS_CHOICES = (
        ("postgres", "PostgreSQL"),
        ("mssql", "Microsoft SQL Server"),
    )

    database_type = models.CharField(max_length=50, default="OrderView")
    server = models.CharField(max_length=200)
    database = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=500)
    port = models.IntegerField(default=1433)
    dbms = models.CharField(
        max_length=50, choices=DBMS_CHOICES, unique=True, default="mssql"
    )
