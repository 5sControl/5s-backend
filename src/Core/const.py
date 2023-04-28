import os


SERVER_URL = os.environ.get("SERVER_URL")

PRODUCTION = os.environ.get("PRODUCTION")
if PRODUCTION is not None and PRODUCTION.lower() == "true":
    PRODUCTION = True
else:
    PRODUCTION = False

print("Server Configuration:")
print(f"SERVER_URL -> {SERVER_URL}")
print(f"PRODUCTION -> {PRODUCTION}")
