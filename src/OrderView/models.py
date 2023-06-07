from django.db import models

from src.CameraAlgorithms.models import Camera


class IndexOperations(models.Model):
    """
    Parameter indeks stanowisko for searching in Winkhouse database
    """

    type_operation = models.IntegerField(verbose_name="id_stanowisko operation control")
    camera = models.OneToOneField(
        Camera, verbose_name="operations_control camera", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "IndexOperatio"
        verbose_name_plural = "IndexOperations"

        db_table = "index_operations"
