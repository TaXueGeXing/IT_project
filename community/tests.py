from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Article, Reply
from rest_framework.authtoken.models import Token

class ArticleTests(APITestCase):
    def setUp(self):
        # 创建测试用户和Token认证
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # 创建测试文章和回复
        self.article = Article.objects.create(title='Test Article', content='Test Content', tag='Test', user=self.user)
        self.reply = Reply.objects.create(article=self.article, content='Test Reply', user=self.user, time='2021-01-01T00:00:00Z')

    def test_community_view(self):
        url = reverse('community_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_article(self):
        url = reverse('create_article')
        data = {'title': 'New Article', 'content': 'New Content', 'tag': 'New Tag'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_reply(self):
        url = reverse('create_reply', kwargs={'pk': self.article.pk})
        data = {'article_id': self.article.pk, 'content': 'Another Reply'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_article_list(self):
        url = reverse('article_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_articles(self):
        url = reverse('search_articles') + '?query=Test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_detail(self):
        url = reverse('article_detail', kwargs={'pk': self.article.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
