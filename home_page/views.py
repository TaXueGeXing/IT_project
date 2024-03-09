from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from community.models import Article
from community.models import Reply
from Transaction.models import Product
from django.db.models import Count
from .serializers import ProductSerializer, ResultSerializer


@api_view(['GET'])
def homepage_view(request):
    if not isinstance(request, HttpRequest):
        request = request._request
    # 获取排名信息
    top_five_models = ranking(request)
    # 获取首页信息
    top_article = Article.objects.order_by('-click').first()
    recent_replies = Reply.objects.order_by('-time')[:5]

    data = {
        'Best-Selling products': top_five_models,
        'Articles': top_article,
        'Discussion': recent_replies
    }
    return Response(ResultSerializer(data).data)


@api_view(['GET'])
def ranking(request):
    # 使用 annotate 和 values 来计算每个型号的订单数量，并按数量降序排列取前五个
    top_models = Product.objects.values('car__car_model', 'car__car_brand').annotate(order_count=Count('order')).order_by('-order_count')[:5]

    return Response(top_models)


@api_view(['GET'])
def search_product(request):#搜索没问题 跳转未知
    # 获取交易页面信息
    #default_products = Product.objects.filter( 默认未知
       # Order__is_finished=False,
        #Order__is_banned=False,
        #Order__buyer_id=None
    #).distinct()

    if request.method == 'GET':
        location = request.GET.get('Location')
        brand = request.GET.get('car_brand')
        car_model = request.GET.get('car_model')
        min_price = request.GET.get('Min_Price')
        max_price = request.GET.get('Max_Price')

        # 处理搜索结果
        result_products = Product.objects.filter(
            car__car_brand__icontains=brand,
            car__car_model__contains=car_model,
            Price__range=[min_price, max_price],
            Location__icontains=location
        )
    else:
        result_products = Product.objects.none()
            #default_products

    serializer = ProductSerializer(result_products, many=True)
    return Response({'result_products': serializer.data})






