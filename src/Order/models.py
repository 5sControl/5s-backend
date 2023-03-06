from django.db import models

class MyModel(models.Model):
    field1 = models.CharField(max_length=50)
    field2 = models.IntegerField()
    
    class Meta:
        using = 'ms_sql'