from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_product, name='create_product'),
    path('pending_orders/', views.view_pending_orders, name='pending_orders'),
    path('buy_product/<int:product_id>/', views.buy_product, name='buy_product'),
    path('order_contact/<int:order_id>/', views.view_order_contact, name='order_contact'),
    path('complete_order/<int:order_id>/', views.complete_order, name='complete_order'),
    # Add more URL patterns as needed
]
