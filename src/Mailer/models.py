from django.db import models
from src.Inventory.models import Items


class SMTPSettings(models.Model):
    """
    Models SMTP server
    """

    server = models.CharField(max_length=255)
    port = models.IntegerField()
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email_use_tls = models.BooleanField(default=False)
    email_use_ssl = models.BooleanField(default=True)

    def __str__(self):
        return self.server


class Messages(models.Model):
    """
    Message to send to email
    """

    subject = models.CharField(max_length=150)
    message = models.TextField()
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    date_updated = models.DateTimeField(verbose_name="Date updated", auto_now=True)

    def __str__(self):
        return self.subject


class Emails(models.Model):
    """
    Email to send notifications
    """

    email = models.EmailField(verbose_name="Email to send notifications")

    def __str__(self):
        return self.email


class Recipients(models.Model):
    """
    Table for a many-to-many relationship
    """

    email = models.ForeignKey(Emails, on_delete=models.CASCADE)
    message = models.ForeignKey(Messages, on_delete=models.CASCADE, related_name='recipients')
    item = models.ForeignKey(Items, related_name='item_id', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.email.email} - {self.message.subject}"


class NotificationsSent(models.Model):
    """
    Model for storing records of sent notifications
    """

    recipients = models.ForeignKey(Recipients, on_delete=models.CASCADE, related_name='notifications')
    date_created = models.DateTimeField(verbose_name="Date created", auto_now_add=True)

    def __str__(self):
        return self.recipients.message.subject
