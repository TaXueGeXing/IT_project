from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('car_wiki/', views.car_wiki, name='car_wiki'),
                  path('search/car/', views.search_car, name='search_car'),
                  path('car_detail/<int:car_id>/', views.car_detail_view, name='car_detail'),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
