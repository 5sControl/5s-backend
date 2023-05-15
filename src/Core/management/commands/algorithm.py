from django.core.management.base import BaseCommand

from src.CameraAlgorithms.models import Algorithm
from src.Core.const import ALGORITHMS


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.create_or_update_algorithms()

    def create_or_update_algorithms(self):
        for algorithms_data in ALGORITHMS:
            algorithm, created = Algorithm.objects.update_or_create(
                name=algorithms_data["name"],
                defaults={
                    "is_available": algorithms_data["is_available"],
                    "description": algorithms_data["description"],
                },
            )
            if created:
                algorithm.save()
