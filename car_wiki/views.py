from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Car
from .serializers import CarSerializer


@api_view(['GET'])
def car_wiki(request):  # Car wiki page
    cars = Car.objects.all()[:3]  # Show three cars on Car wiki page
    serializer = CarSerializer(cars, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_car(request):
    if request.method == 'GET':
        brand = request.GET.get('car_brand')  # Get car brand
        car_model = request.GET.get('car_model')  # Get car model

        result_car = Car.objects.get(car_brand=brand, car_model=car_model)  # Get the matching car object
        serializer = CarSerializer(result_car)
        return Response(serializer.data)


@api_view(['GET'])
def car_detail_view(request, car_id):
    car = get_object_or_404(Car, car_id=car_id)   # Get the specified car object with car id, If not, return 404 NOT FOUND
    serializer = CarSerializer(car)
    return Response(serializer.data)
