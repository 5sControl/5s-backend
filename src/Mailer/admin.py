from django.contrib import admin
from src.Mailer.models import Emails, SMTPSettings, WorkingTime, WorkingTimeDaysOfWeek


@admin.register(Emails)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("email", "id", 'is_active')


@admin.register(WorkingTime)
class WorkingTimeAdmin(admin.ModelAdmin):
    list_display = ('time_start', 'time_end', 'id')


@admin.register(SMTPSettings)
class SMTPSettingsAdmin(admin.ModelAdmin):
    list_display = ("server", "port", "username", "password", "email_use_tls", "email_use_ssl", "id")


@admin.register(WorkingTimeDaysOfWeek)
class WorkingTimeDaysOfWeekAdmin(admin.ModelAdmin):
    list_display = ("day_of_week", "working_time")
    list_filter = ("day_of_week", "working_time")
    search_fields = ("day_of_week__day", "working_time__time_start", "working_time__time_end")
