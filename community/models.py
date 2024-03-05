from django.db import models
from django.contrib.auth.models import User

# Create your models here.
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