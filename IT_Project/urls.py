"""
URL configuration for IT_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ranking/', views.home, name='home'),
    path('carwiki/', views.carwiki, name='carwiki'),
    path('search/car/', views.search_car, name='search_car'),
    path('car_detail/<str:car_id>/', views.car_detail, name='car_detail'),
    path('search/product/', views.search_product, name='search_product'),
    path('about-us/', views.about_us, name='about_us'),
]
