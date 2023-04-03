from django.db import models


class IndexOperations(models.Model):
    """
    Parameter type of operation in the customer database
    """

    type_operation = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.type_operation}"
