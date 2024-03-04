from django.db import models

class User(models.Model):
    UserID = models.CharField(max_length=8)
    UserName = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    Email = models.EmailField()
    PhoneNo = models.IntegerField()
    Picture = models.ImageField()

class Article(models.Model):
    ArticleID = models.CharField(max_length=8)
    UserID = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.CharField(max_length=100)
    Content = models.TextField()
    Tag = models.CharField(max_length=30)

class Reply(models.Model):
    ReplyID = models.CharField(max_length=8)
    ArticleID = models.ForeignKey(Article, on_delete=models.CASCADE)
    Time = models.DateTimeField()

class Car(models.Model):
    CarID = models.CharField(max_length=8)
    Type = models.CharField(max_length=30)
    Define = models.CharField(max_length=30)
    Brand = models.CharField(max_length=30)

class Product(models.Model):
    ProductID = models.CharField(max_length=8)
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    Date = models.DateField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField()
    Title = models.CharField(max_length=100)

class Order(models.Model):
    OrderID = models.CharField(max_length=8)
    BuyerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders')
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    Time = models.DateTimeField()
    IsBanned = models.BooleanField()
    IsFinished = models.BooleanField()
    IsAgreed = models.BooleanField()

# Create your models here.
