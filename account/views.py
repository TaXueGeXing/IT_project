from django.contrib.auth.decorators import login_required
from .models import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from Transaction.models import *

def register(request):
    if request.method == 'POST':
        # 从 POST 请求中获取用户提交的数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        # 其他字段的获取类似

        # 创建新的用户对象并保存到数据库中
        user = User.objects.create(
            UserName=username,
            Password=password,
            Email=email,
            PhoneNo=phone_number,
            # 其他字段类似
        )
        # 可以在这里添加一些额外的逻辑，比如发送欢迎邮件等

        # 重定向到账户页面或其他页面
        return redirect('account')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account')  # 登录成功后重定向到用户资料页面或其他页面
        else:
            # 登录失败，返回登录页面并显示错误消息
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')  # 注销后重定向到登录页面

@login_required
def edit_profile(request):
    if request.method == 'POST':
        # 从 POST 请求中获取用户修改的信息
        user = request.user
        user.UserName = request.POST.get('username')
        user.Email = request.POST.get('email')
        user.PhoneNo = request.POST.get('phone_number')
        # 其他字段的获取类似

        # 保存修改后的用户信息到数据库中
        user.save()

        # 重定向到个人资料页面或其他页面
        return redirect('account')
    else:
        return render(request, 'edit_profile.html', {'user': request.user})

@login_required
def view_order_history(request):
    # 获取当前用户的所有订单信息
    orders = Order.objects.filter(BuyerID=request.user)
    return render(request, 'order_history.html', {'orders': orders})