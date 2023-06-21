from django.db import models


class FiltrationOperationsTypeID(models.Model):
    operation_type_id = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "filtration_operations"
