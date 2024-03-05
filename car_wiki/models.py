from django.db import models


class Car(models.Model):
    carID = models.AutoField(primary_key=True)
    carModel = models.TextField()
    define = models.TextField()
    brand = models.TextField()

