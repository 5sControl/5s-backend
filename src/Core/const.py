import os

from decouple import config

SERVER_URL = os.environ.get("SERVER_URL")
if not SERVER_URL:
    SERVER_URL = config("SERVER_URL")

PRODUCTION = os.environ.get("PRODUCTION")
if PRODUCTION is not None and PRODUCTION.lower() == "true":
    PRODUCTION = True
else:
    PRODUCTION = False
