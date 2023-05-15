from django.db import models
from src.Cameras.models import Camera


class Items(models.Model):
    """Models items"""

    name = models.TextField(max_length=75, verbose_name="Item name")
    status = models.CharField(max_length=20, default="Out of stock")
    current_stock_level = models.IntegerField(verbose_name="Current stock level", default=0)
    low_stock_level = models.IntegerField(verbose_name="Low stock level", default=0)
    camera = models.ForeignKey(Camera, related_name='camera_id', on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    coords = models.JSONField(verbose_name="Area coordinates")
    prev_status = models.TextField(verbose_name="Previous status", default=None, max_length=30, blank=True, null=True)
    multi_row = models.BooleanField(verbose_name="Multi row", default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_update = bool(self.pk)
        camera_updated = self.pk and self.camera_id != self.__class__.objects.get(pk=self.pk).camera_id
        coords_updated = self.pk and self.coords != self.__class__.objects.get(pk=self.pk).coords

        try:
            previous_camera = Items.objects.get(id=self.pk).camera_id
        except Exception as e:
            print(e)

        instance = super().save(*args, **kwargs)

        if not is_update or camera_updated or coords_updated:

            # stopped process
            from src.Inventory.service import stopped_process, started_process
            items_camera = Items.objects.filter(camera_id=self.camera)
            if len(items_camera) > 0:
                stopped_process(self.camera)

            # started process
            started_process(self.camera)

            # restart process
            if camera_updated:
                stopped_process(previous_camera)
                started_process(previous_camera)

        return instance

    def delete(self, *args, **kwargs):
        instance = super().delete(*args, **kwargs)

        # stopped process
        from src.Inventory.service import stopped_process, started_process
        stopped_process(self.camera)

        # started process if there are more than 0 items
        items_camera = Items.objects.filter(camera_id=self.camera)
        if len(items_camera) > 0:

            started_process(self.camera)

        return instance
