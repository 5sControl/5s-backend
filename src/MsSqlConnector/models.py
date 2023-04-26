import base64
import os

from django.db import models

from cryptography.fernet import Fernet


class DatabaseConnection(models.Model):
    database_type = models.CharField(max_length=50, default="OrderView")
    server = models.CharField(max_length=200)
    database = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password = models.BinaryField()
    port = models.IntegerField(default=1433)

    def get_password(self):
        key = os.environ.get("HASH")
        key_bytes = base64.urlsafe_b64decode(key.encode())
        f = Fernet(key_bytes)
        password = f.decrypt(self.password).decode()
        return password

    def set_password(self, password):
        key = os.environ.get("HASH")
        f = Fernet(key)
        self.password = f.encrypt(password.encode())

    password = property(get_password, set_password)
