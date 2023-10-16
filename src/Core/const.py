import os

from decouple import config

ONVIF_SERVICE_URL = config("ONVIF_SERVICE_URL")
ONVIFFINDER_SERVICE_URL = config("ONVIFFINDER_SERVICE_URL")
ALGORITHMS_CONTROLLER_SERVICE_URL = config("ALGORITHMS_CONTROLLER_SERVICE_URL")
DJANGO_SERVICE_URL = config("DJANGO_SERVICE_URL")
SERVER_URL = config("SERVER_URL")
if SERVER_URL is not None:
    ONVIF_SERVICE_URL = SERVER_URL
    ONVIFFINDER_SERVICE_URL = SERVER_URL
    ALGORITHMS_CONTROLLER_SERVICE_URL = SERVER_URL
    DJANGO_SERVICE_URL = SERVER_URL
else:
    ONVIF_SERVICE_URL = "http://" + ONVIF_SERVICE_URL
    ONVIFFINDER_SERVICE_URL = "http://" + ONVIFFINDER_SERVICE_URL
    ALGORITHMS_CONTROLLER_SERVICE_URL = "http://" + ALGORITHMS_CONTROLLER_SERVICE_URL
    DJANGO_SERVICE_URL = "http://" + DJANGO_SERVICE_URL

EMULATE_DB = os.environ.get("EMULATE_DB")
if EMULATE_DB is not None and EMULATE_DB.lower() == "true":
    EMULATE_DB = True
else:
    EMULATE_DB = False

safety_control_ear_protection_description = """
Designed to ensure that the workers in a particular area are wearing ear protection to safeguard their hearing.
This control is important in environments where workers are exposed to loud noises that could damage their hearing over time.
"""
safety_control_head_protection_description = """
Designed to ensure that workers are wearing safety helmets to protect their heads from potential hazards.
This control is crucial in construction sites, mining areas, and other hazardous workplaces where head injuries are common.
"""
safety_control_hand_protection_description = """
Designed to ensure that workers are wearing protective gloves to prevent hand injuries.
This control is essential in workplaces where the workers are exposed to sharp objects, chemicals, or high-temperature materials that could cause burns or cuts.
"""
safety_control_reflective_jacket_description = """
Designed to ensure that workers are wearing reflective jackets to increase their visibility and reduce the risk of accidents caused by low visibility.
This control is critical in workplaces where workers are exposed to low light conditions, such as construction sites, mining areas, or transportation facilities.
"""
machine_control_description = """
Is designed to ensure that the machine is not left unsupervised, which could lead to accidents, breakdowns, or other issues (downtime & lost profits).
This control is essential in workplaces where machines are used, such as factories, construction sites, or warehouses.
"""

ALGORITHMS = [
    {
        "name": "idle_control",
        "image_name": "5scontrol/idle_python:latest",
        "is_available": True,
        "description": None
    },
    {
        "name": "operation_control",
        "image_name": "5scontrol/operation_control_js:latest",
        "is_available": False,
        "description": None
    },
    {
        "name": "machine_control",
        "image_name": "5scontrol/machine_control_python:latest",
        "is_available": True,
        "description": machine_control_description,
    },
    {
        "name": "machine_control_js",
        "image_name": "5scontrol/machine_control_js:latest",
        "is_available": True,
        "description": machine_control_description + " (JS)",
    },
    {
        "name": "safety_control_ear_protection",
        "image_name": None,
        "is_available": False,
        "description": safety_control_ear_protection_description,
    },
    {
        "name": "safety_control_head_protection",
        "image_name": None,
        "is_available": False,
        "description": safety_control_head_protection_description,
    },
    {
        "name": "safety_control_hand_protection",
        "image_name": None,
        "is_available": False,
        "description": safety_control_hand_protection_description,
    },
    {
        "name": "safety_control_reflective_jacket",
        "image_name": None,
        "is_available": False,
        "description": safety_control_reflective_jacket_description,
    },
    {
        "name": "min_max_control",
        "image_name": "5scontrol/min_max_python:latest",
        "is_available": True,
        "description": None
    },
]
