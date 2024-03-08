from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Article(models.Model):
    article_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=100)
    content = models.TextField()
    tag = models.CharField(max_length=30)
    created_time = models.DateTimeField(auto_now_add=True)
    click = models.IntegerField(default=0)


class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies')
    content = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)


