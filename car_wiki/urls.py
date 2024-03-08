from django.urls import path
from .views import car_wiki, search_car, car_detail_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
                  path('api/car_wiki/', car_wiki, name='car_wiki'),
                  path('api/search_car/', search_car, name='search_car'),
                  path('api/car_detail/<int:car_id>/', car_detail_view, name='car_detail'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
