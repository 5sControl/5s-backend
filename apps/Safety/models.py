from django.db import models


class Action(models.Model):
    """Action safety control"""

    image = models.TextField(verbose_name='Image action')
    action = models.TextField(verbose_name='Action')
    name_file = models.TextField(verbose_name='Name pickle file', blank=True, null=True)
    camera = models.TextField(verbose_name='Camera')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.action

    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'
