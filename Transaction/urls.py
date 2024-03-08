from django.urls import path
from Transaction.views import ProductListCreateAPIView, BuyProductAPIView, FinishOrderAPIView


urlpatterns = [
    # API视图
    path('api/products/', ProductListCreateAPIView.as_view(), name='product_list_create'),
    path('api/buy/', BuyProductAPIView.as_view(), name='buy_product'),
    path('api/finishOrder/', FinishOrderAPIView.as_view(), name='finish_order'),
]

