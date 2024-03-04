from django.db import models

class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    Email = models.EmailField()
    PhoneNo = models.IntegerField()
    Picture = models.ImageField()

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

class Product(models.Model):
    ProductID = models.AutoField(primary_key=True)
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    Date = models.DateField()
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField()
    Title = models.CharField(max_length=100)

class Order(models.Model):
    OrderID = models.AutoField(primary_key=True)
    BuyerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_orders')
    SellerID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_orders')
    ProductID = models.ForeignKey(Product, on_delete=models.CASCADE)
    Time = models.DateTimeField()
    IsBanned = models.BooleanField()
    IsFinished = models.BooleanField()
    IsAgreed = models.BooleanField()

# Create your models here.
