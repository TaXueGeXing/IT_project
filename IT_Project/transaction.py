from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone

@login_required
def create_product(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        price = request.POST.get('price')
        description = request.POST.get('description')
        
        # create Product
        product = Product.objects.create(
            Title=title,
            Date=date,
            Price=price,
            Description=description,
            SellerID=request.user,
        )
        
        # create Order (BuyerID will set up when Someone wanna to buy it)
        order = Order.objects.create(
            BuyerID=None,
            SellerID=request.user,
            ProductID=product,
            Time=timezone.now(),
            IsBanned=False,  # Defuat
            IsFinished=False,  # Defuat
            IsAgreed=False,  # Defuat
        )
        
        return redirect('product_detail', product_id=product.id)
    else:
        return render(request, 'create_product.html')

def view_pending_orders(request):
    # IsFinished=False(Not be selled), IsBanned=False(not be baned), BuyerID=None(No one wanna buy is now)
    pending_orders = Order.objects.filter(IsFinished=False, IsBanned=False, BuyerID=None)
    return render(request, 'pending_orders.html', {'pending_orders': pending_orders})

@login_required
def buy_product(request, product_id):
    if request.method == 'POST':

        # get informations
        buyer = request.user
        product = Product.objects.get(id=product_id)
        
        try:
            # check the order
            order = Order.objects.get(ProductID=product, BuyerID=None)
            
            # update it
            order.BuyerID = buyer
            order.Time = timezone.now()
            order.save()
            
            return redirect('product_detail', product_id=product_id)
        except Order.DoesNotExist:
            return redirect('product_detail', product_id=product_id)
    else:
        return render(request, 'buy_product.html', {'product_id': product_id})
