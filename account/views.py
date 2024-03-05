from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Transaction.models import *
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
        )
        user.save()
        return redirect('order_history')
    else:
        return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
    if user:
        login(request, user)
        return redirect('order_history')
    else:
        return render(request, 'login.html', {'error_message': 'Invalid username or password'})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.save()

        return redirect('order_history')
    else:
        return render(request, 'edit_profile.html', {'user': request.user})

@login_required
def order_history(request):
    orders = Order.objects.filter(BuyerID=request.user)
    return render(request, 'order_history.html', {'orders': orders})