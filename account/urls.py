from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('order-history/', views.view_order_history, name='order_history'),
]