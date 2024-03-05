from django.urls import path
from . import views
urlpatterns = [
    path('ranking/', views.home, name='home'),
    path('search/product/', views.search_product, name='search_product'),
]
