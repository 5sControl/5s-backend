import logging
from django.core.management.base import BaseCommand
from src.DatabaseConnections.models import ConnectionInfo

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create connection for erp-service."

    def handle(self, *args, **options):
        try:
            connection, created = ConnectionInfo.objects.get_or_create(
                erp_system="5s_control",
                defaults={
                    "type": "api",
                    "dbms": "postgres",
                    "is_active": True,
                    "host": "http://erp-service",
                    "server": None,
                    "database": None,
                    "username": "admin",
                    "password": "admin",
                    "port": 3005,
                    "used_in_orders_view": True,
                },
            )

            if created:
                logger.info("Connection created successfully.")
                self.stdout.write(self.style.SUCCESS("✅ Connection created successfully."))
            else:
                logger.info("Connection already exists.")
                self.stdout.write(self.style.SUCCESS("ℹ️ Connection already exists."))

        except Exception as e:
            logger.error(f"Error creating connection: {e}")
            self.stdout.write(self.style.ERROR(f"❌ Error creating connection: {e}"))
