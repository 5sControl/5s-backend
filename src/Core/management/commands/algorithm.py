from django.core.management.base import BaseCommand

from src.Algorithms.models import Algorithm


safety_control_ear_protection_description = """
designed to ensure that the workers in a particular area are wearing ear protection to safeguard their hearing.
This control is important in environments where workers are exposed to loud noises that could damage their hearing over time.
"""
safety_control_head_protection_description = """
designed to ensure that workers are wearing safety helmets to protect their heads from potential hazards.
This control is crucial in construction sites, mining areas, and other hazardous workplaces where head injuries are common.
"""
safety_control_hand_protection_description = """
designed to ensure that workers are wearing protective gloves to prevent hand injuries.
This control is essential in workplaces where the workers are exposed to sharp objects, chemicals, or high-temperature materials that could cause burns or cuts.
"""
safety_control_reflective_jacket_description = """
designed to ensure that workers are wearing reflective jackets to increase their visibility and reduce the risk of accidents caused by low visibility.
This control is critical in workplaces where workers are exposed to low light conditions, such as construction sites, mining areas, or transportation facilities.
"""
machine_control_description = """
is designed to ensure that the machine is not left unsupervised, which could lead to accidents, breakdowns, or other issues (downtime & lost profits).
This control is essential in workplaces where machines are used, such as factories, construction sites, or warehouses.
"""


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.ALGORITHMS = [
            {"name": "idle_control", "is_available": True, "description": ""},
            {"name": "operation_control", "is_available": True, "description": ""},
            {"name": "machine_control", "is_available": True, "description": machine_control_description},
            {"name": "safety_control_ear_protection", "is_available": True, "description": safety_control_ear_protection_description},
            {"name": "safety_control_head_protection", "is_available": False, "description": safety_control_head_protection_description},
            {"name": "safety_control_hand_protection", "is_available": False, "description": safety_control_hand_protection_description},
            {"name": "safety_control_reflective_jacket", "is_available": True, "description": safety_control_reflective_jacket_description},
            {"name": "min_max_control", "is_available": True, "description": ""},
        ]
        self.create_algorithms()

    def create_algorithms(self):
        for algorithms_data in self.ALGORITHMS:
            if Algorithm.objects.filter(name=algorithms_data["name"]).first():
                continue
            else:
                algorithms = Algorithm.objects.create(
                    name=algorithms_data["name"],
                    is_available=algorithms_data["is_available"],
                    description=algorithms_data["description"]
                )
                algorithms.save()