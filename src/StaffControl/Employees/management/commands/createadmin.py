from django.core.management.base import BaseCommand

from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create a superuser"

    def handle(self, *args, **options):
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "admin@example.com", "admin")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Superuser created successfully. Username: admin Password: admin"
                )
            )
        else:
            self.stdout.write(self.style.WARNING("Superuser already exists"))
