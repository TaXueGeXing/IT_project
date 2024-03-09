from django.db import models


class Car(models.Model):
    car_id = models.AutoField(primary_key=True)
    car_model = models.CharField(max_length=30)
    car_brand = models.CharField(max_length=30)
    class Meta:
        app_label = 'car_wiki'


class CarDetail(models.Model):
    car = models.OneToOneField(Car, on_delete=models.PROTECT, related_name='car_detail')
    define = models.TextField()
    picture = models.ImageField(upload_to='images', blank=True, null=True)
    class Meta:
        app_label = 'car_wiki'



