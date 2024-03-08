from rest_framework import serializers
from Transaction.models import Product, Order
from car_wiki.models import Car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    car = CarSerializer()

    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
