from django.urls import path
from . import views

urlpatterns = [
    path('community/', views.community_view, name='community_view'),
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/<int:pk>/replies/create/', views.create_reply, name='create_reply'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/search/', views.search_articles, name='search_articles'),
    path('articles/<int:pk>/', views.article_detail, name='article_detail'),
]