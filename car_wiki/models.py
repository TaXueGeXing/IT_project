from django.db import models

# Create your models here.
class Car(models.Model):
    carID = models.CharField(max_length=8)
    car_model = models.TextField()
    define = models.TextField()
    brand = models.TextField()
