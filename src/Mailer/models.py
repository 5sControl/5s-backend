from django.db import models


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

    def save(self, *args, **kwargs):
        from src.Mailer.service import test_smtp_settings
        test = test_smtp_settings(self)
        if type(test) == bool:
            super().save(*args, **kwargs)
        else:
            raise ValueError('SMTP configuration is incorrect')


class Emails(models.Model):
    """
    Email to send notifications
    """

    email = models.EmailField(verbose_name="Email to send notifications")
    is_active = models.BooleanField(default=True, verbose_name="Is activ email")

    def __str__(self):
        return self.email


class DayOfWeek(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = models.CharField(max_length=20, choices=DAY_CHOICES)

    def __str__(self):
        return self.day


class WorkingTime(models.Model):
    """
    Working time MinMax
    """

    time_start = models.TimeField(verbose_name="Start time")
    time_end = models.TimeField(verbose_name="End time")
    days_of_week = models.ManyToManyField(DayOfWeek, blank=True, null=True)

    def __str__(self):
        return f"{self.time_end} - {self.time_start}"

