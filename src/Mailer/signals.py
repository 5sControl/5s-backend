from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import DayOfWeek


@receiver(post_migrate)
def create_days_of_week(sender, **kwargs):
    if sender.name == 'src.Mailer':
        if not DayOfWeek.objects.exists():
            DayOfWeek.objects.create(day="Monday")
            DayOfWeek.objects.create(day="Tuesday")
            DayOfWeek.objects.create(day="Wednesday")
            DayOfWeek.objects.create(day="Thursday")
            DayOfWeek.objects.create(day="Friday")
            DayOfWeek.objects.create(day="Saturday")
            DayOfWeek.objects.create(day="Sunday")
