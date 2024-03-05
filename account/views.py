from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from Transaction.models import *
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create(
            UserName=username,
            Password=password,
            Email=email,
        )
        user.save()
        return redirect('account')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(UserName=username, Password=password)
        if user.exists():
            login(request, user.first())
            return redirect('account')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    else:
        return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.UserName = request.POST.get('username')
        user.Email = request.POST.get('email')
        user.save()

        return redirect('account')
    else:
        return render(request, 'edit_profile.html', {'user': request.user})

@login_required
def view_order_history(request):
    orders = Order.objects.filter(BuyerID=request.user)
    return render(request, 'order_history.html', {'orders': orders})