import os
from django.db import models

from cryptography.fernet import Fernet


class DatabaseConnection(models.Model):
    database_type = models.CharField(max_length=50, default="OrderView")
    server = models.CharField(max_length=200)
    database = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    password_encrypted = models.BinaryField()
    port = models.IntegerField(default=1433)

    def get_password(self):
        key = os.environ.get("HASH")
        f = Fernet(key)
        password = f.decrypt(self.password_encrypted).decode()
        return password

    def set_password(self, password):
        key = os.environ.get("HASH")
        f = Fernet(key)
        self.password_encrypted = f.encrypt(password.encode())

    password = property(get_password, set_password)
