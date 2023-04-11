from django.contrib import admin
from src.Mailer.models import Emails, Recipients, Messages, SMTPSettings


@admin.register(Emails)
class EmailAdmin(admin.ModelAdmin):
    list_display = ("email", "id",)


@admin.register(Recipients)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("item", "email", "message", "id")


@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ("subject", "message", "date_created", "date_updated", "id",)


@admin.register(SMTPSettings)
class SMTPSettingsAdmin(admin.ModelAdmin):
    list_display = ("server", "port", "username", "password", "email_use_tls", "email_use_ssl", "id")
