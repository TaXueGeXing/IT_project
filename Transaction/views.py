from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import *
from django.utils import timezone
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

@login_required
def create_product(request):
    logger.debug("111111111111111111111111")
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        price = request.POST.get('price')
        description = request.POST.get('description')
        # user = request.POST.get('user')

        logger.debug(f"Received POST request to create product with title={title}, date={date}, price={price}, description={description}")

        # create Product
        product = Product.objects.create(
            Title=title,
            Date=date,
            Price=price,
            Description=description,
            SellerID=request.user
        )
        logger.info(f"Product created successfully with title={title}, id={product.ProductID}")

        # create Order
        order = Order.objects.create(
            BuyerID=None,
            SellerID=request.user,
            ProductID=product,
            Time=timezone.now(),
            IsBanned=False,
            IsFinished=False,
            IsAgreed=False,
        )

        logger.info(f"Order created successfully for product with id={product.ProductID}")
        return redirect('pending_orders/', product_id=product.ProductID)
    else:
        return render(request, 'create_product.html')

def view_pending_orders(request):
    # IsFinished=False(Not be selled), IsBanned=False(not be baned), BuyerID=None(No one wanna buy is now)
    pending_orders = Order.objects.filter(IsFinished=False, IsBanned=False, BuyerID=None)
    response_content = 'Pending orders: {}'.format(pending_orders)
    return HttpResponse(response_content)
    # return render(request, 'pending_orders.html', {'pending_orders': pending_orders})

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


def view_order_contact(request, order_id):

    order = get_object_or_404(Order, id=order_id)
    if order.IsAgreed and not order.IsBanned: #Check order is available
        # get connections
        buyer_contact = order.BuyerID.Email, order.BuyerID.PhoneNo
        seller_contact = order.SellerID.Email, order.SellerID.PhoneNo
        
        return render(request, 'order_details.html', {'order': order, 'buyer_contact': buyer_contact, 'seller_contact': seller_contact})
    else:
        return render(request, 'order_not_available.html')

def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    order.IsFinished = True
    order.save()
    
    return redirect('order_detail', order_id=order_id)
# Create your views here.
