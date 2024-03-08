from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Transaction.models import Order
from django.contrib.auth.hashers import check_password

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'register.html')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'register.html')

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('login')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_profile')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        # 更改密码操作
        if 'change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password1 = request.POST.get('new_password1')
            new_password2 = request.POST.get('new_password2')

            if not check_password(old_password, user.password):
                messages.error(request, "Old password is incorrect.")
            elif new_password1 != new_password2:
                messages.error(request, "New passwords do not match.")
            else:
                user.set_password(new_password1)
                user.save()
                messages.success(request, "Your password was successfully updated!")

        # 更新个人资料操作（示例：更改用户名）
        elif 'update_profile' in request.POST:
            # 假设表单提交的是个人资料更新
            new_username = request.POST.get('username', user.username)
            new_email = request.POST.get('email', user.email)
            # 简单的数据验证逻辑
            if User.objects.filter(username=new_username).exclude(pk=user.pk).exists():
                messages.error(request, 'Username already taken.')
            elif User.objects.filter(email=new_email).exclude(pk=user.pk).exists():
                messages.error(request, 'Email already registered.')
            else:
                user.username = new_username
                user.email = new_email
                user.save()
                messages.success(request, 'Profile updated successfully.')
        # 这里不重定向，以便在更新资料后保持在同一页，并显示更新结果

        # 获取订单历史
        elif 'order_history' in request.POST:
            orders = Order.objects.filter(BuyerID=user)
            return render(request, 'user_dashboard.html', {'orders': orders})