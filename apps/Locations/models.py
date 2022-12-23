from django.db import models


class Cameras(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Gate(models.Model):
    name = models.CharField(max_length=30)
    camera_input = models.ForeignKey(Cameras, related_name='DeviceInput', on_delete=models.CASCADE)
    camera_output = models.ForeignKey(Cameras, related_name='DeviceOutput', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=30)
    gate_id = models.ForeignKey(Gate, related_name='Gate', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
