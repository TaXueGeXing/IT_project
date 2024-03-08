from django.urls import path
from . import views

urlpatterns = [
    path('community', views.article_list, name='article_list'),
    path('article_list', views.article_list, name='article_list'),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('create/', views.create_article, name='create_article'),
    path('article/<int:article_id>/reply/', views.create_reply, name='create_reply')
]