from django.shortcuts import render, redirect
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from . import models
from .models import Article
from .models import Comment
from .models import Product


def homepage_view(request):
    # 在首页视图函数中调用 ranking_view 获取排名信息
    top_five_models = ranking()
    # 调用首页文章和讨论区 'Discussion & Articles': 'Some other data'
    top_article = Article.objects.order_by('-clicks').first
    # 实时滚动评论区
    recent_comments = Comment.objects.order_by('-create_time')[:5]
    # 传递排名信息和其他信息到首页
    context = {'Best-Selling products': top_five_models, 'Articles': top_article, 'Discussion': recent_comments}
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
        postcode = request.GET.get('postcode')
        distance_value = request.GET.get('distance')
        brand = request.GET.get('brand')
        car_model = request.GET.get('carModel')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        longitude, latitude = map(float, postcode.split(' '))
        # 创建 Point 对象表示地理位置
        user_location = Point(longitude, latitude)
        # 处理搜索结果
        result_products = models.Product.objects.filter(
            # 根据实际情况调整筛选条件
            car_brand__icontains=brand,
            car__carModel__icontains=car_model,
            price__range=[min_price, max_price],
            # 计算比对distance 通过postcode
            location__distance_lte=(user_location, D(mi=distance_value))
        )

    # 将搜索结果传递给交易页面
    return redirect('transaction', result_products=result_products)


def transaction_view(request):
    # 获取默认产品（根据实际情况调整）
    default_products = models.Product.objects.filter(is_default=True)

    # 获取搜索结果
    result_products = request.session.get('result_products', None)

    # 如果没有搜索结果，使用默认产品
    if result_products is None:
        result_products = default_products

    context = {'result_products': result_products}
    return render(request, 'transaction.html', context)


def home(request):
    return render(request, 'home.html')


def carwiki(request):
    return render(request, 'carwiki.html')


def about_us(request):
    return render(request, 'about_us.html')


def carwiki_view(request):
    # 获取默认产品（最新发布的五种车）
    default_cars = models.Car.objects.filter(is_default=True).order_by('-create_time')[:5]
    # 获取搜索结果
    result_car = request.session.get('result_car', None)

    # 如果没有搜索结果，使用默认产品
    if result_car is None:
        result_car = default_cars

    context = {'result_car': result_car}

    return render(request, 'carwiki.html', context)


def search_car(request):
    # 处理搜索请求
    if request.method == 'GET':
        brand = request.GET.get('brand')
        car_model = request.GET.get('car_model')

        # 处理搜索结果
        result_car = models.Car.objects.filter(
            # 根据实际情况调整筛选条件
            brand__icontains=brand,
            car_model__icontains=car_model,
        )
        if result_car.exists():
            car_id = result_car.first().carID
            return redirect('car_detail', car_id=car_id)

    else:
        result_car = None
    request.session['result_car'] = result_car
    return redirect('carwiki', result_car=result_car)
