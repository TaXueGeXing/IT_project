from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Car, CarDetail
from .serializers import CarSerializer


@api_view(['GET'])
def car_wiki(request):
    cars = Car.objects.all()
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_car(request):
    if request.method == 'GET':
        brand = request.GET.get('car_brand')
        car_model = request.GET.get('car_model')

        result_car = Car.objects.get(car_brand=brand, car_model=car_model)
        serializer = CarSerializer(result_car)
        return Response(serializer.data)


@api_view(['GET'])
def car_detail_view(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)
    serializer = CarSerializer(car)
    return Response(serializer.data)
