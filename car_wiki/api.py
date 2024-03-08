from rest_framework import viewsets
from .models import Car
from .serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
