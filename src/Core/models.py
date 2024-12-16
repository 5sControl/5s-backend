from django.db import models


#
class CustomPermission(models.Model):
    codename = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'auth_permission_custom'
        verbose_name = 'Custom Permission'
        verbose_name_plural = 'Custom Permissions'

    def __str__(self):
        return self.name


class SystemMessage(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "System message"
        verbose_name_plural = "System message"
        db_table = "system_message"

