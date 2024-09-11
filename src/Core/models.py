from django.db import models


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

