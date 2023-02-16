from django.core.management.base import BaseCommand

from src.Algorithms.models import Algorithm


class Command(BaseCommand):
    """
    Fill table with available algorithms
    """

    def handle(self, *args, **options):
        self.ALGORITHMS = [
            {"name": "Staff_Control", "is_available": False},
            {"name": "Idle_Control", "is_available": True},
            {"name": "Tool_Control", "is_available": False},
            {"name": "Machine_Control", "is_available": True},
            {"name": "Safety_Control_Ear_protection", "is_available": True},
            {"name": "Safety_Control_Head_protection", "is_available": False},
            {"name": "Safety_Control_Hand_protection", "is_available": False},
            {"name": "Safety_Control_Reflective_jacket", "is_available": False},
        ]
        self.algorithms_was_exist = 0
        self.algorithms_was_created = 0
        self.create_algorithms()
        self.stdout.write(
            self.style.SUCCESS(f"{self.algorithms_was_exist} - was exist")
        )
        self.stdout.write(
            self.style.SUCCESS(f"{self.algorithms_was_created} - was created")
        )

    def create_algorithms(self):
        for algorithms_data in self.ALGORITHMS:
            if Algorithm.objects.filter(name=algorithms_data["name"]).first():
                self.stdout.write(
                    self.style.WARNING(f"algorithms {algorithms_data['name']} exist")
                )
                self.algorithms_was_exist += 1
                continue
            else:
                algorithms = Algorithm.objects.create(
                    name=algorithms_data["name"],
                    is_available=algorithms_data["is_available"],
                )
                algorithms.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"algorithms {algorithms_data['name']} was successfully created"
                )
            )
            self.algorithms_was_created += 1
