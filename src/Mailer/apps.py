from django.apps import AppConfig


class MailerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.Mailer"

    def ready(self):
        import src.Mailer.signals
