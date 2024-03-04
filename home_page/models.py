from django.db import models

# Create your models here.
class Product(models.Model):
    productID = models.CharField(max_length=8)
    time = models.DateTimeField()
    price = models.IntegerField()
    description = models.TextField()
    title = models.TextField()
    sellerID = models.CharField(max_length=8)
    # car = models.ForeignKey("Car", on_delete=models.CASCADE)
    # 关联？ 我暂时调整了代码，因为这行代码会导致报错


class Article(models.Model):
    articleID = models.CharField(max_length=8)
    title = models.TextField()


class Comment(models.Model):
    commentID = models.CharField(max_length=8)
