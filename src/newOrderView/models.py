from django.db import models


class FiltrationOperationsTypeID(models.Model):
    operation_type_id = models.IntegerField(unique=True, null=True, blank=True)
    name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    type_erp = models.CharField(max_length=50, default=None, null=True, blank=True)

    class Meta:
        db_table = "filtration_operations"
