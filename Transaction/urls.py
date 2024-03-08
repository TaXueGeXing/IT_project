from django.urls import path
from Transaction.views import ProductListCreateAPIView, BuyProductAPIView


urlpatterns = [
    # API视图
    path('api/products/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('buy/<int:product>/', BuyProductAPIView.as_view(), name='buy_product'),
]

