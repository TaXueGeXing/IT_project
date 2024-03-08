from rest_framework import serializers
from Transaction.models import Product
from car_wiki.serializers import CarSerializer


class ProductSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Product
        fields = ['ProductID', 'SellerID', 'Date', 'Price', 'Description', 'Title', 'car', 'Location']
