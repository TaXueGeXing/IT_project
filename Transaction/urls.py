from django.urls import path
from Transaction.views import ProductListCreateAPIView, OrderListCreateAPIView


urlpatterns = [
    # API视图
    path('api/products/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('api/orders/', OrderListCreateAPIView.as_view(), name='order_list_create'),
]

