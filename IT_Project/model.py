from django.db import models

from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse


class Car(models.Model):
    carID = models.CharField(max_length=8)
    carModel = models.TextField()
    define = models.TextField()
    brand = models.TextField()

    def get_absolute_url(self):

        return redirect(reverse('car_detail', args=[str(self.carID)]))


class Product(models.Model):
    productID = models.CharField(max_length=8)
    time = models.DateTimeField()
    price = models.IntegerField()
    description = models.TextField()
    title = models.TextField()
    sellerID = models.CharField(max_length=8)
    car = models.ForeignKey("Car", on_delete=models.CASCADE)
    # 关联？


class Article(models.Model):
    articleID = models.CharField(max_length=8)
    title = models.TextField()


class Comment(models.Model):
    commentID = models.CharField(max_length=8)
