from django.db import models

class Car(models.Model):
    CarID = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=30)
    Define = models.CharField(max_length=30)
    Brand = models.CharField(max_length=30)

# Create your models here.

