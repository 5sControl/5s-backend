#!/usr/bin/env python
import os
import sys

from src.Core.const import PRODUCTION, SERVER_URL


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    print("Server Configuration:")
    print(f"SERVER_URL -> {SERVER_URL}")
    print(f"PRODUCTION -> {PRODUCTION}")


if __name__ == "__main__":
    main()
