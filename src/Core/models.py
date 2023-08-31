from django.db import models


class SystemMessage(models.Model):
    id = models.AutoField(primary_key=True, db_index=True)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
