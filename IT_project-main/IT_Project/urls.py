"""
URL configuration for IT_Project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('transactions/', views.view_transactions, name='view_transactions'),
    path('transactions/<int:pk>/', views.transaction_detail, name='transaction_detail'),
    path('search-by-tag/', views.search_by_tag, name='search_by_tag'),

    path('change-password/', auth_views.PasswordChangeView.as_view(
        template_name='change_password.html',
        success_url='/profile/'  # 假设密码更改成功后重定向到个人资料页面
    ), name='change_password'),

    path('posts/', views.CarPostListView.as_view(), name='carpost_list'),  # 显示所有帖子的列表
    path('posts/new/', views.create_carpost, name='create_carpost'),
    path('posts/<int:pk>/', views.carpost_detail, name='carpost_detail'),
]