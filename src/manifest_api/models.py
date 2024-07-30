from django.db import models
import requests


class ManifestConnection(models.Model):
    host = models.CharField(max_length=200)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100, null=True, blank=True)
    token = models.CharField(max_length=500, blank=True)
    status = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    #reportd to manigest
    asset_class_id = models.IntegerField(null=True, blank=True)
    asset_id = models.IntegerField(null=True, blank=True)
    location_id = models.IntegerField(null=True, blank=True)
    job_template = models.IntegerField(null=True, blank=True)
    assigned_user = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.host} - {self.username}"

    def save(self, *args, **kwargs):
        if not self.token:
            token = self._get_token()
            if token:
                self.token = token
                self.password = None
                self.status = True
                super().save(*args, **kwargs)
            else:
                raise ValueError("Failed to log in.")
        else:
            super().save(*args, **kwargs)

    def _get_token(self):
        url = f"{self.host}rest/signin"
        data = {
            'email': self.username,
            'password': self.password
        }
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'PostmanRuntime/7.37.3',
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            token = response_data.get('user').get('token')
            return token
        except requests.exceptions.RequestException as e:
            print(f"Error while requesting token: {e}")
            return None
