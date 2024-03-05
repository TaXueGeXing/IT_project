from django.db import models

# Create your models here.
class User(models.Model):
    UserID = models.AutoField(primary_key=True)
    UserName = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    Email = models.EmailField()
    PhoneNo = models.IntegerField()
    Picture = models.ImageField()
