from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from .models import Product, Order, Car
from django.contrib.auth.models import User
from .serializers import ProductSerializer, OrderSerializer
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse

class ProductListCreateAPIViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpass')
        self.car_t = Car.objects.create(car_brand='Toyota', car_model='Camry')
        self.product = Product.objects.create(
            Title='Test Product',
            SellerID=self.user,
            Date='2023-01-01',
            Price='20.00',
            Description='A description of the product',
            car=self.car_t,
            Location='Product Location'
        )
        self.order = Order.objects.create(
            BuyerID=None,
            SellerID=self.user,
            ProductID=self.product,
            Time=timezone.now(),
            IsBanned=False,
            IsFinished=False,
            IsAgreed=False,
        )

    def test_product_list_anonymous_user(self):
        url = reverse('product_list_create')  # 使用 reverse() 函数生成 URL 路径
        response = self.client.get(url)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        #print(response.data)

    def test_product_list_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product_list_create')  # 使用 reverse() 函数生成 URL 路径
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        #print(response.data)

    def test_product_create_anonymous_user(self):
        url = reverse('product_list_create')  # 使用 reverse() 函数生成 URL 路径
        data = {
            'Title': 'New Product',
            'SellerID': self.user,
            'Date': '2023-01-02',
            'Price': '20.00',
            'Description': 'A description of the new product',
            'car': self.car_t, 
            'Location': 'New Product Location'
        }
        response = self.client.post(url, data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_product_create_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('product_list_create')  # 使用 reverse() 函数生成 URL 路径
        data = {
            'Title': 'New Product',
            'Date': '2023-01-03',
            'Price': '20.00',
            'Description': 'A description of the new product',
            'Location': 'New Product Location',
            'car_brand': 'Toyota',
            'car_model': 'Camry'
        }
        # serializer = ProductSerializer(data)
        # print(serializer.is_valid())
        response = self.client.post(url, data)
        print(response.context)
        products = Product.objects.all()
        for product in products:
            # 在这里对产品对象进行操作
            print(product.ProductID)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(Product.objects.all()), 2)
        orders = Order.objects.all()
        for order in orders:
            # 在这里对产品对象进行操作
            print(order.OrderID)
        url = reverse('buy_product')  # 使用 reverse() 函数生成 URL 路径，传入产品的主键
        data = {'product': 1}
        response_buy = self.client.post(url, data)
        print("buy_product",response_buy)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('finish_order')  # 使用 reverse() 函数生成 URL 路径，传入产品的主键
        data = {'order_pk': 1}
        response_buy = self.client.post(url, data)
        print("finish",response_buy)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # 现在可以对购买后的行为进行检查，比如检查订单是否已经创建等等
        orders = Order.objects.all()
        for order in orders:
            # 在这里对产品对象进行操作
            print(order.OrderID)
            print(order.BuyerID)
            print(order.IsFinished)

    # def test_buy_product_authenticated_user(self):
    #     self.client.force_authenticate(user=self.user)
    #     url = reverse('buy_product', kwargs={'product': self.product.pk})  # 使用 reverse() 函数生成 URL 路径，传入产品的主键
    #     response = self.client.post(url)
    #     print(response)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # 现在可以对购买后的行为进行检查，比如检查订单是否已经创建等等
    #     orders = Order.objects.all()
    #     for order in orders:
    #         # 在这里对产品对象进行操作
    #         print(order.OrderID)
    #     # self.assertTrue(Order.objects.filter(BuyerID=self.user, ProductID=self.product).exists())

