from django.db import models


class Car(models.Model):
    CarID = models.AutoField(primary_key=True)
    CarModel = models.CharField(max_length=30)
    Brand = models.CharField(max_length=30)


class CarDetail(models.Model):
    Car = models.OneToOneField(Car, on_delete=models.PROTECT, related_name='car_detail', primary_key=True)
    Define = models.CharField(max_length=30)


class Image(models.Model):
    CarDetail = models.ForeignKey(CarDetail, on_delete=models.CASCADE, related_name='images')
    picture = models.ImageField(upload_to='images', blank=True, null=True)


