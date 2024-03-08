from rest_framework import serializers
from .models import Car, CarDetail, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('picture',)


class CarDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = CarDetail
        fields = ('define', 'images')


class CarSerializer(serializers.ModelSerializer):
    car_detail = CarDetailSerializer()

    class Meta:
        model = Car
        fields = ('car_model', 'car_brand', 'car_detail')
