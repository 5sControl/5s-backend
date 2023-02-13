from django.core.management.base import BaseCommand

from src.Algorithms.models import Algorithm


class Command(BaseCommand):
    """
    Fill table with available algorithms
    """

    def handle(self, *args, **options):
        self.AlLGORITHMS = [
            "Staff_Control",
            "Idle_Control",
            "Tool_Control",
            "Safety_Control_Ear_protection",
            "Safety_Control_Head_protection",
            "Safety_Control_Hand_protection",
            "Safety_Control_Reflective_jacket",
        ]
        self.create_algorithms()
        print("[INFO] Success!")

    def create_algorithms(self):
        for algorithm in self.AlLGORITHMS:
            algorithms = Algorithm.objects.create(name=algorithm)

            algorithms.save()
            print(f"[INFO] algorithms {algorithm} was successfully created")
