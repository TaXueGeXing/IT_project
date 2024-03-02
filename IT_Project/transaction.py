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
        
        # 创建商品对象并保存到数据库
        product = Product.objects.create(
            Title=title,
            Date=date,
            Price=price,
            Description=description,
            SellerID=request.user,
        )
        
        # 创建订单对象并保存到数据库
        order = Order.objects.create(
            BuyerID=None,  # 设置买家为空
            SellerID=request.user,  # 卖家为当前登录用户
            ProductID=product,
            Time=timezone.now(),  # 使用当前时间作为订单时间
            IsBanned=False,  # 默认订单不被禁止
            IsFinished=False,  # 默认订单未完成
            IsAgreed=False,
        )
        
        return redirect('product_detail', product_id=product.id)  # 重定向到新创建商品的详情页面
    else:
        return render(request, 'create_product.html')

def view_pending_orders(request):
    # 查询所有未完成、未被禁止且买家为空的订单
    pending_orders = Order.objects.filter(IsFinished=False, IsBanned=False, BuyerID=None)
    
    # 将查询结果传递给模板进行展示
    return render(request, 'pending_orders.html', {'pending_orders': pending_orders})

