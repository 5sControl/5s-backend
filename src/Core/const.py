import os


SERVER_URL = os.environ.get("SERVER_URL")
PRODUCTION = os.environ.get("PRODUCTION")

print("Server Configuration:")
print(f"SERVER_URL -> {SERVER_URL}")
print(f"PRODUCTION -> {PRODUCTION}")
