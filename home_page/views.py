from django.shortcuts import render, redirect
from community.models import Article
from community.models import Reply
from Transaction.models import Product




def home_page(request):
    return render(request, 'home.html')


def homepage_view(request):
    # 在首页视图函数中调用 ranking_view 获取排名信息
    top_five_models = ranking()
    # 调用首页文章和讨论区 'Discussion & Articles': 'Some other data'
    top_article = Article.objects.order_by('-clicks').first
    # 实时滚动评论区
    recent_replies = Reply.objects.order_by('-create_time')[:5]
    # 传递排名信息和其他信息到首页
    context = {'Best-Selling products': top_five_models, 'Articles': top_article, 'Discussion': recent_replies}
    if request.method == 'POST':
        # 调用 search_product 处理搜索，并将结果存储在 session 中
        search_product(request)
        # 重定向到交易页面
        return redirect('transaction')
    return render(request, 'homepage.html', context)


def ranking():
    # 获取所有产品
    all_products = Product.objects.all().order_by('-orders_count')

    # 前5名productModel
    top_five_models = []

    for product in all_products:
        if product.carModel not in top_five_models:
            top_five_models.append(product.carModel)
            # 够五个
            if len(top_five_models) == 5:
                break

    return top_five_models


def search_product(request):
    # 处理搜索请求
    result_products = None
    if request.method == 'GET':
        location = request.GET.get('location')
        brand = request.GET.get('brand')
        car_model = request.GET.get('carModel')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # 处理搜索结果
        result_products = (Product.objects.filter(
            car_brand__icontains=brand,
            car__carModel__icontains=car_model,
            price__range=[min_price, max_price],
            location__icontains=location
        ))

    # 将搜索结果传递给交易页面
    return redirect('transaction', result_products=result_products)


def transaction_view(request):
    # 获取默认产品（根据实际情况调整）
    default_products = Product.objects.filter(is_default=True)

    # 获取搜索结果
    result_products = request.session.get('result_products', None)

    # 如果没有搜索结果，使用默认产品
    if result_products is None:
        result_products = default_products

    context = {'result_products': result_products}
    return render(request, 'transaction.html', context)

