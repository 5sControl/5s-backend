from django.core.management.base import BaseCommand

from src.Algorithms.models import Algorithms


class Command(BaseCommand):
    """
    Fill table with available algorithms
    """

    def handle(self, *args, **options):
        self.AlLGORITHMS = [
            "Staff Control",
            "Idle Control",
            "Tool Control",
            "Safety Control: Ear protection",
            "Safety Control: Head protection",
            "Safety Control: Hand protection",
            "Safety Control: Reflective jacket",
        ]
        self.create_algorithms()
        print("[INFO] Success!")

    def create_algorithms(self):
        for algorithm in self.AlLGORITHMS:
            algorithms = Algorithms.objects.create(name=algorithm)

            algorithms.save()
            print(f"[INFO] algorithms {algorithm} was successfully created")
