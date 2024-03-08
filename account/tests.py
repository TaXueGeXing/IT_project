from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class AccountTests(APITestCase):

    def setUp(self):
        # 创建一个用户以便测试登录和更新个人资料
        self.user = User.objects.create_user(username='testuser', password='testpassword123')
        self.token = Token.objects.create(user=self.user)
        
        # 对于需要认证的请求，设置认证信息
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_register_user(self):
        """
        测试用户注册
        """
        url = reverse('register')
        data = {'username': 'newuser', 'password': 'newuser123', 'email': 'newuser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_token_login(self):
        """
        测试用户使用用户名和密码登录
        """
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('token' in response.data)

    def test_logout(self):
        """
        测试用户登出
        """
        url = reverse('logout')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
    def test_change_password(self):
        """
        测试修改密码
        """
        url = reverse('change_password')
        data = {'old_password': 'testpassword123', 'new_password': 'newpassword456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 测试用新密码登录
        self.client.logout()
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'newpassword456'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_profile(self):
        """
        测试更新个人资料
        """
        url = reverse('update_profile')
        data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updateduser@example.com')

    def test_order_history(self):
        """
        测试查看订单历史
        """
        url = reverse('order_history')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
