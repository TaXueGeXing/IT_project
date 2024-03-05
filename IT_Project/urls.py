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
from account import views as auth_view
from community import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('ranking/', views.home, name='home'),
    path('carwiki/', views.carwiki, name='carwiki'),
    path('search/car/', views.search_car, name='search_car'),
    path('car_detail/<str:car_id>/', views.car_detail, name='car_detail'),
    path('search/product/', views.search_product, name='search_product'),
    path('about-us/', views.about_us, name='about_us'),

    path('register/', auth_view.register, name='register'),
    path('login/', auth_view.user_login, name='login'),
    path('logout/', auth_view.user_logout, name='logout'),
    path('edit-profile/', auth_view.edit_profile, name='edit_profile'),
    path('order-history/', auth_view.view_order_history, name='order_history'),
    path('community/', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('create/', views.create_article, name='create_article'),
    path('article/<int:article_id>/reply/', views.create_reply, name='create_reply')
]
