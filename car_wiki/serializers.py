from rest_framework import serializers
from .models import Car, CarDetail


class CarDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CarDetail
        fields = ('define', 'picture')


class CarSerializer(serializers.ModelSerializer):
    car_detail = CarDetailSerializer()

    class Meta:
        model = Car
        fields = ('car_model', 'car_brand', 'car_detail')
