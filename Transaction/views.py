# views.py
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Product, Order, Car
from .serializers import ProductSerializer, OrderSerializer


class ProductListCreateAPIView(APIView):
    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response({'error': 'You must be authenticated to create a product.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        car = Car.objects.create(
            car_brand = request.data.get('car_brand'),
            car_model = request.data.get('car_model')
        )

        product = Product.objects.create(
            Title = request.data.get('Title'),
            Date = request.data.get('Date'),
            Price = request.data.get('Price'),
            Description = request.data.get('Description'),
            Location = request.data.get('Location'),
            SellerID = request.user,
            car = car
        )
        
        product.SellerID = request.user
        product.save()
        order = Order.objects.create(
            BuyerID=None,
            SellerID=request.user,
            ProductID=product,
            Time=timezone.now(),
            IsBanned=False,
            IsFinished=False,
            IsAgreed=False,
        )
        # serializer = ProductSerializer(data=request.data)
        # logger.debug(request.data)
        # if serializer.is_valid():
        #     serializer.save(SellerID=request.user)
        return Response(status=status.HTTP_201_CREATED)


class BuyProductAPIView(APIView):
    def post(self, request, format=None):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response({'error': 'You must be authenticated to create a product.'}, status=status.HTTP_401_UNAUTHORIZED)
        product = request.data.get('product')
        order = Order.objects.get(ProductID = product)
        order.BuyerID = request.user
        order.save()
        # serializer = ProductSerializer(data=request.data)
        # logger.debug(request.data)
        # if serializer.is_valid():
        #     serializer.save(SellerID=request.user)
        return Response(status=status.HTTP_201_CREATED)

class FinishOrderAPIView(APIView):
    def post(self, request, format=None):
        self.permission_classes = [IsAuthenticated]
        if not request.user.is_authenticated:
            return Response({'error': 'You must be authenticated to create a product.'}, status=status.HTTP_401_UNAUTHORIZED)
        order_pk = request.data.get('order_pk')
        order = Order.objects.get(OrderID = order_pk)
        order.IsFinished = True
        order.save()
        # serializer = ProductSerializer(data=request.data)
        # logger.debug(request.data)
        # if serializer.is_valid():
        #     serializer.save(SellerID=request.user)
        return Response(status=status.HTTP_201_CREATED)
# 更多视图...



# from django.shortcuts import render
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from .models import *
# from django.utils import timezone
# from django.http import HttpResponse
# import logging

# logger = logging.getLogger(__name__)

# @login_required
# def create_product(request):
#     logger.debug("111111111111111111111111")
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         date = request.POST.get('date')
#         price = request.POST.get('price')
#         description = request.POST.get('description')

#         car_model = request.POST.get('car_model')
#         brand = request.POST.get('brand')
#         location = request.POST.get('location')
#         # user = request.POST.get('user')

#         logger.debug(f"Received POST request to create product with title={title}, date={date}, price={price}, description={description}")
        
#         try:
#             Car.objects.get(CarModel = car_model)
#         except:
#             car_c = Car.objects.create(
#                 CarModel = car_model,
#                 Brand = brand
#             )

#         # create Product
#         product = Product.objects.create(
#             Title=title,
#             Date=date,
#             Price=price,
#             Description=description,
#             SellerID=request.user,
#             Location = location,
#             car = car_c
#         )
#         logger.info(f"Product created successfully with title={title}, id={product.ProductID}")

#         # create Order
#         order = Order.objects.create(
#             BuyerID=None,
#             SellerID=request.user,
#             ProductID=product,
#             Time=timezone.now(),
#             IsBanned=False,
#             IsFinished=False,
#             IsAgreed=False,
#         )

#         logger.info(f"Order created successfully for product with id={product.ProductID}")
#         return redirect('pending_orders/', product_id=product.ProductID)
#     else:
#         return render(request, 'create_product.html')

# def view_pending_orders(request):
#     # IsFinished=False(Not be selled), IsBanned=False(not be baned), BuyerID=None(No one wanna buy is now)
#     pending_orders = Order.objects.filter(IsFinished=False, IsBanned=False, BuyerID=None)
#     response_content = 'Pending orders: {}'.format(pending_orders)
#     return HttpResponse(response_content)
#     # return render(request, 'pending_orders.html', {'pending_orders': pending_orders})

# @login_required
# def buy_product(request, product_id):
#     if request.method == 'POST':
#         logger.debug(f"buy_product_now")

#         # get informations
#         buyer = request.user
#         product = Product.objects.get(id=product_id)
        
#         # try:
#             # check the order
#         order = Order.objects.get(ProductID=product_id, BuyerID=None)
            
#         # update it
#         order.BuyerID = buyer
#         order.Time = timezone.now()
#         order.save()
            
#         return redirect('order_contact', product_id=product_id)
#         # except Order.DoesNotExist:
#         #     return redirect('order_contact', product_id=product_id)
#     else:
#         return HttpResponse()
#         return render(request, 'buy_product.html', {'product_id': product_id})


# def view_order_contact(request, order_id):

#     order = get_object_or_404(Order, id=order_id)
#     if order.IsAgreed and not order.IsBanned: #Check order is available
#         # get connections
#         buyer_contact = order.BuyerID.Email, order.BuyerID.PhoneNo
#         seller_contact = order.SellerID.Email, order.SellerID.PhoneNo
        
#         return render(request, 'order_details.html', {'order': order, 'buyer_contact': buyer_contact, 'seller_contact': seller_contact})
#     else:
#         return render(request, 'order_not_available.html')

# def complete_order(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
    
#     order.IsFinished = True
#     order.save()
    
#     return redirect('order_detail', order_id=order_id)
# # Create your views here.



