from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from Transaction.models import Product
from car_wiki.models import Car


class ProductSearchTestCase(TestCase):
    def setUp(self):
        # 创建测试数据
        self.client = APIClient()
        self.user1 = User.objects.create(username='user1', password='password1', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', password='password1', email='user1@example.com')
        self.user3 = User.objects.create(username='user3', password='password3', email='user1@example.com')
        car1 = Car.objects.create(car_brand='Brand1', car_model='Model1')
        car2 = Car.objects.create(car_brand='Brand2', car_model='Model2')
        car3 = Car.objects.create(car_brand='Brand3', car_model='Model3')
        self.product1 = Product.objects.create(SellerID=self.user1, Date='2022-01-01', Price=100, Description='Some description1', Title='1Some title', car=car1, Location='Location1')
        self.product2 = Product.objects.create(SellerID=self.user2, Date='2022-01-03', Price=200, Description='Some description2', Title='S2ome title', car=car2, Location='Location2')
        self.product3 = Product.objects.create(SellerID=self.user3, Date='2022-01-02', Price=110, Description='Some description3', Title='So3me title', car=car3, Location='Location3')

    def test_search_product(self):
        query_params = {
            'car_brand': 'Brand1',
            'car_model': 'Model1',
            'Min_Price': 50,
            'Max_Price': 120,
            'Location': 'Location1',
        }

        url = reverse('search_product')  # 替换成你的视图名称，可能是 'search_product' 或其他实际的名称
        response = self.client.get(url, query_params)

        # 发送 GET 请求

        print(response.content)
        print("Request URL:", url)
        # 断言 HTTP 状态码为 200
        self.assertEqual(response.status_code, 200)

        # 获取返回的数据
        result_products = response.json().get('result_products', [])

        print("Result Products:", result_products)


        # 断言返回的数据符合预期
        self.assertEqual(result_products[0]['car']['car_brand'], 'Brand1')

        self.assertEqual(result_products[0]['Price'], "100.00")  # 注意这里的数据类型，不再是字符串
        self.assertEqual(result_products[0]['Location'], 'Location1')
