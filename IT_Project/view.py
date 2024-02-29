

from django.shortcuts import render, HttpResponse

from . import models
from .models import Product
from .models import Article
from .models import Comment

def homepage_view(request):
    # 在首页视图函数中调用 ranking_view 获取排名信息
    top_five_models = ranking(request)
    # 调用首页文章和讨论区 'Discussion & Articles': 'Some other data'
    top_article = Article.objects.order_by('-clicks').first
    #实时滚动评论区
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    #recent_comments = get_recent_comments()
    search_products = search_product(request)

    # 传递排名信息和其他信息到首页
    context = {'Best-Selling products': top_five_models, 'Articles': top_article, 'Discussion': recent_comments, 'Search': search_products}
    return render(request, 'homepage.html', context)

def search_product(request):
    # 处理搜索请求(参考交易的改）
    if request.method == 'GET':
        postcode = request.GET.get('postcode')
        distance_value = request.GET.get('distance')
        brand = request.GET.get('brand')
        carModel = request.GET.get('carModel')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        # 处理搜索结果
        search_results = models.Product.objects.filter(
            # 根据实际情况调整筛选条件
            description__icontains=brand|carModel,
            price__in=[min_price, max_price],
            #计算比对distance 通过postcode

        )
    else:
        search_results = None

    # 传递数据到 Transaction 页面模板
    context = {'search_results': search_results,}
    return render(request, 'transaction.html', context)

def ranking(request):
    # 获取所有产品
    all_products = Product.objects.all().order_by('-orders_count')

    # 前5名productModel
    top_five_models = []

    for product in all_products:
            if product.carModel not in top_five_models:
                top_five_models.append(product.carModel)
            #够五个
            if len(top_five_models) == 5:
                break

    return top_five_models



def home(request):
    return render(request, 'Home.html')
def transaction(request):
    return render(request, 'Transaction.html')
def carwiki(request):
    return render(request, 'carwiki.html')
def community(request):
    return render(request, 'Community.html')
def about_us(request):
    return render(request, 'About us.html')
def web_information(request):
    return render(request, 'web_information.html')
def support(request):
    return render(request, 'support.html')
def account(request):
    return render(request, 'My Account.html')

def search_car(request):
    # 处理搜索请求
    if request.method == 'GET':
        brand = request.GET.get('brand')
        carModel = request.GET.get('carModel')

        # 处理搜索结果
        result_car = models.Car.objects.filter(
            # 根据实际情况调整筛选条件
            brand__icontains = brand,
            carModel__icontains = carModel,
        )
    else:
        result_car = None
    context = {'result_car': result_car }

    return render(request, 'carwiki.html',result_car)
