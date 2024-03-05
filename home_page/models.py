from django.db import models
from account.models import User


class Car(models.Model):
    carID = models.CharField(max_length=8)
    carModel = models.TextField()
    define = models.TextField()
    brand = models.TextField()


class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    time = models.DateTimeField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    Title = models.CharField(max_length=100)
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    car = models.ForeignKey("Car", on_delete=models.PROTECT)
    #我暂时调整了代码，因为这行代码会导致报错

class Article(models.Model):
    ArticleID = models.AutoField(primary_key=True)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Content = models.TextField()
    Tag = models.CharField(max_length=30)


class Reply(models.Model):
    ReplyID = models.AutoField(primary_key=True)
    ArticleID = models.ForeignKey(Article, on_delete=models.CASCADE)
    Time = models.DateTimeField()
