from django.urls import path
from . import views
urlpatterns = [
    path('ranking/', views.ranking, name='home'),
    path('search/product/', views.search_product, name='search_product'),
]
