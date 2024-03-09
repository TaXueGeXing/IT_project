from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

class AccountTests(APITestCase):

    def setUp(self):
        # 创建一个用户以便测试登录和更新个人资料
        self.user = User.objects.create_user(username='testuser', password='testpassword123', email='testuser@example.com')
        self.token = Token.objects.create(user=self.user)
        
        # 对于需要认证的请求，设置认证信息
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        #print(f"Created token for testuser: {self.token.key}")
        
    def test_register_user(self):
        """
        测试用户注册
        """
        print("\n\n===== 测试用户注册 =====")
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newuser123', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        print(f"注册用户响应: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_login(self):
        """
        测试用户使用用户名和密码登录
        """
        print("\n\n===== 测试用户登录 =====")
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        print(f"登录响应Token: {response.data.get('token', '无Token返回')}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data['token']

        # 使用获取的token访问受保护的视图
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        
        # 获取受保护视图的 URL
        protected_view_url = reverse('order_history')
    
        # 尝试访问受保护的视图
        response = self.client.get(protected_view_url)
        # 验证是否成功访问受保护的视图
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("用户成功登录，并使用token访问了受保护的视图。")
    
    def test_logout(self):
        """
        测试用户登出
        """
        print("\n\n===== 测试用户登出 =====")
        url = reverse('logout')
        response = self.client.post(url, format='json')
        print(f"登出响应状态: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_change_password(self):
        """
        测试修改密码
        """
        print("\n\n===== 测试修改密码 =====")
        url = reverse('change_password')
        data = {'old_password': 'testpassword123', 'new_password': 'newpassword456'}
        response = self.client.post(url, data, format='json')
        print("修改密码响应状态: 200 成功")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 测试用新密码登录
        self.client.logout()
        print("测试使用新密码登录...")
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'newpassword456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        """
        测试更新个人资料
        """
        print("\n\n===== 测试更新个人资料 =====")
        url = reverse('update_profile')
        data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
        response = self.client.post(url, data, format='json')
        print(f"更新资料响应: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        print(f"更新后的用户名: {self.user.username}, 邮箱: {self.user.email}")
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_order_history(self):
        """
        测试查看订单历史
        """
        print("\n\n===== 测试查看订单历史 =====")
        url = reverse('order_history')
        response = self.client.get(url, format='json')
        print(f"订单历史响应: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
