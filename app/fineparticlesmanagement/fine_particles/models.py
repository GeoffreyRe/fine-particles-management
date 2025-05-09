from django.db import models

class Unit(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MeasurementType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Measurement(models.Model):
    time = models.DateTimeField()
    value = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    type = models.ForeignKey(MeasurementType, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.value} {self.unit} at {self.time}"
