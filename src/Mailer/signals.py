from django.db.models.signals import post_migrate, m2m_changed

from django.dispatch import receiver

from .models import DayOfWeek, WorkingTime
from .service import work_time_min_max


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


@receiver(m2m_changed, sender=WorkingTime.days_of_week.through)
def handle_days_of_week_change(sender, instance, action, reverse, model, pk_set, **kwargs):
    time_start = instance.time_start
    time_end = instance.time_end
    days = []
    if action == 'post_add' and not reverse:
        for day_id in pk_set:
            day = DayOfWeek.objects.get(pk=day_id)
            days.append(day)

