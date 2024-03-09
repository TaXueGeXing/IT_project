from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', token_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('change-password/', change_password, name='change_password'),
    path('update-profile/', update_profile, name='update_profile'),
    path('order-history/', order_history, name='order_history'),
]
