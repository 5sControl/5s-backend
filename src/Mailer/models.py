from django.db import models


class SMTPSettings(models.Model):
    """
    Models SMTP server
    """

    server = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

