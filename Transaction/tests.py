from django.test import TestCase
from django.urls import reverse  # 导入User模型
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Product, Order

class CreateProductViewTest(TestCase):
    def setUp(self):
        # 创建一个用户实例并保存到数据库中
        self.user = User.objects.create_user(
            username="testUser",
            password="123456789",
            email="123@test.com",
        )
        # 使用 force_login 方法登录用户
        self.client.force_login(self.user)

    def test_create_product_post(self):

        # 准备用于POST请求的数据
        post_data = {
            'title': 'Test Product',
            'date': '2024-03-01',
            'price': '20.00',
            'description': 'This is a test product.',
            'car_model': 'SUV',
            'brand': 'BYD',
            'location': 'Glasgow'
        }
        
        # 检查用户是否登录
        if self.client.session.get('_auth_user_id'):
            print("User is logged in.")
        else:
            print("User is not logged in.")

        print(post_data)
        # 发送POST请求
        # for i in range(10):
        #     post_data = {
        #         'title': 'Test Product '+str(i),
        #         'date': '2024-03-01',
        #         'price': '20.00',
        #         'description': 'This is a test product. '+str(i)
        #     }
        #     response = self.client.post(reverse('create_product'), data=post_data)

        response = self.client.post(reverse('create_product'), data=post_data)
        
        # 检查产品是否成功创建
        print(len(Order.objects.all()))
        self.assertEqual(response.status_code, 302)  # 302表示重定向
        self.assertTrue(Product.objects.filter(Title=post_data['title']).exists())
        print("len:  ", len(Product.objects.all()))

        print("Existing Products in the Database:")
        for product in Product.objects.all():
            print("Product Title:", product.Title)
            print("Product Date:", product.Date)
            print("Product Price:", product.Price)
            print("Product Description:", product.Description)
            print("Product Seller:", product.SellerID.username)
            print()  # 添加一个空行以提高可读性.SellerID.username)
            print()  # 添加一个空行以提高可读性

        orders = Order.objects.all()
        for order in orders:
            print("Order ID:", order.OrderID)
            print("Buyer ID:", order.BuyerID.username if order.BuyerID else "None")
            print("Seller ID:", order.SellerID.username)
            print("Product Title:", order.ProductID.Title)
            print("Time:", order.Time)
            print("Is Banned:", order.IsBanned)
            print("Is Finished:", order.IsFinished)
            print("Is Agreed:", order.IsAgreed)
            print("Email:", order.SellerID.email)
            print()  # 添加一个空行以提高可读性
        
        response = self.client.get(reverse('pending_orders'))

        # 检查响应状态码
        self.assertEqual(response.status_code, 200)
        # 检查响应内容是否包含预期的字符串
        self.assertIn('Pending orders:', response.content.decode())
        response_text = response.content.decode()
        print(response_text)

