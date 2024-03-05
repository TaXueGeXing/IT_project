from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
                  path('car_wiki/', views.car_wiki, name='car_wiki'),
                  path('search/car/', views.search_car, name='search_car'),
                  path('car_detail/<str:car_id>/', views.car_detail, name='car_detail'),
              ]