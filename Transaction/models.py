from django.db import models
from django.contrib.auth.models import User
from car_wiki.models import Car

class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    Date = models.DateField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField()
    Title = models.CharField(max_length=100)
    car = models.ForeignKey(Car, on_delete=models.PROTECT, null=True, blank=True)

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    BuyerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders', null=True, blank=True)
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    Time = models.DateTimeField()
    IsBanned = models.BooleanField()
    IsFinished = models.BooleanField()
    IsAgreed = models.BooleanField()

# Create your models here.
