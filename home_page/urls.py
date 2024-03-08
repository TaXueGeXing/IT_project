from django.urls import path
from .views import homepage_view, search_product, ranking

urlpatterns = [
    path('homepage/', homepage_view, name='homepage'),
    path('search/product/', search_product, name='search_product'),
    path('ranking/', ranking, name='home'),
]
