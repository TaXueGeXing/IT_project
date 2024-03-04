from django.db import models

class Car(models.Model):
    CarID = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=30)
    Define = models.CharField(max_length=30)
    Brand = models.CharField(max_length=30)

# Create your models here.
class Car(models.Model):
    carID = models.CharField(max_length=8)
    car_model = models.TextField()
    define = models.TextField()
    brand = models.TextField()
