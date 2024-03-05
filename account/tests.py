from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class AccountTests(TestCase):
    def setUp(self):
        # 创建一个用户用于登录和编辑个人资料的测试
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com', 
            password='testpassword')
        self.client.force_login(self.user)

    def test_register(self):
        # 测试用户注册功能
        self.assertEqual(User.objects.count(), 1)
        self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'newpassword123',
            'email': 'newuser@example.com',
        })
        # 检查用户数量是否增加
        self.assertEqual(User.objects.count(), 2)

        new_user = User.objects.filter(username='newuser').exists()
        self.assertTrue(new_user)

    def test_user_login(self):
        # 测试用户登录功能
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        # 检查是否成功登录
        self.assertEqual(response.status_code, 200)


    def test_user_logout(self):
        # 测试用户登出功能
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        # 检查是否重定向到登录页面
        self.assertRedirects(response, reverse('login'))

    def test_edit_profile(self):
        # 测试编辑个人资料功能
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('edit_profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
        })
        self.assertTrue(response.status_code, 200)
        updated_user = get_user_model().objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, 'updated@example.com')

    def test_view_order_history(self):
        # 测试查看订单历史功能
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order_history'))
        # 检查是否成功访问订单历史页面
        self.assertEqual(response.status_code, 200)
