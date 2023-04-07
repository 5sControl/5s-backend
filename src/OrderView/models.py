from django.db import models
from django.db.models.signals import pre_save

from django.core.exceptions import ValidationError


class IndexOperations(models.Model):
    """
    Parameter type of operation in the customer database
    """

    type_operation = models.IntegerField(default=2)

    def __str__(self):
        return f"{self.type_operation}"


def save_only_one(sender, instance, **kwargs):
    """
    Signal receiver function that ensures only one instance of IndexOperations model is saved
    """
    if instance.pk:
        # If object already exists, allow updating
        return

    if sender.objects.count() > 0:
        # If object doesn't exist yet but there are already other objects, don't save
        raise ValidationError("Only one instance of IndexOperations model is allowed")


# Connect the signal to the model's save method
pre_save.connect(save_only_one, sender=IndexOperations)
