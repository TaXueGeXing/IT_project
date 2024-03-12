from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from community.models import Article
from community.models import Reply
from Transaction.models import Product
from django.db.models import Count
from .serializers import HomepageSerializer
from Transaction.serializers import ProductSerializer


@api_view(['GET'])
def homepage_view(request):
    # If the request object is not an instance of HttpRequest, convert it to the original request object
    if not isinstance(request, HttpRequest):
        request = request._request
    # Get top_five_models, top_article and recent_replies
    top_five_models = ranking(request)
    top_article = Article.objects.order_by('-click').first()
    recent_replies = Reply.objects.order_by('-time')[:5]

    data = {  # Assemble the data
        'Best-Selling products': top_five_models,
        'Articles': top_article,
        'Discussion': recent_replies
    }  # Serialize the data and return it as a response
    return Response(HomepageSerializer(data).data)


@api_view(['GET'])
def ranking(request):
    # Use annotate and value to calculate the order quantity of each model, and sort the top five in descending order of quantity
    top_models = Product.objects.values(
        'car__car_model', 'car__car_brand').annotate(
        order_count=Count('order')).order_by('-order_count')[:5]

    return Response(top_models)


@api_view(['GET'])
def search_product(request):
    # Default trading product list
    default_products = Product.objects.filter(  # Un-traded products are the default products
        Order__is_finished=False,
        Order__is_banned=False,
        Order__buyer_id=None
    ).distinct()[:10]

    if request.method == 'GET':
        # Get location, car brand, car_model, price range as keywords
        location = request.GET.get('Location')
        brand = request.GET.get('car_brand')
        car_model = request.GET.get('car_model')
        min_price = request.GET.get('Min_Price')
        max_price = request.GET.get('Max_Price')

        # Get result cars
        result_products = Product.objects.filter(
            car__car_brand__icontains=brand,
            car__car_model__contains=car_model,
            Price__range=[min_price, max_price],
            Location__icontains=location
        )
    else:
        result_products = default_products  # Show default products

    serializer = ProductSerializer(result_products, many=True)
    return Response({'result_products': serializer.data})
