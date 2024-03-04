from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name

class CarPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='car_posts')
    tags = models.ManyToManyField(Tag, related_name='car_posts')
    title = models.CharField(max_length=100)
    content = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    mileage = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(CarPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Transaction(models.Model):
    buyer = models.ForeignKey(User, related_name='transactions_as_buyer', on_delete=models.CASCADE)
    seller = models.ForeignKey(User, related_name='transactions_as_seller', on_delete=models.CASCADE)
    car_post = models.ForeignKey(CarPost, on_delete=models.CASCADE)
    price_agreed = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=[('pending', 'Pending'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction for {self.car_post.title} between {self.buyer.username} and {self.seller.username}"

