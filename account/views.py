from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from Transaction.models import Order
from .serializers import UserRegisterSerializer, UserProfileSerializer
from Transaction.serializers import OrderSerializer

# 用户注册
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'message': 'User created successfully', 'token': token.key}, status=201)
    return Response(serializer.errors, status=400)

# Token 认证的登录视图
@api_view(['POST'])
@permission_classes([AllowAny])
def token_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=201)
    else:
        return Response({'error': 'Invalid username or password'}, status=400)

# 用户登出
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully logged out.'}, status=204)

# 修改密码
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old_password = request.data.get('old_password')
    new_password = request.data.get('new_password')

    if not user.check_password(old_password):
        return Response({'error': 'Old password is incorrect.'}, status=400)

    user.set_password(new_password)
    user.save()
    return Response({'message': 'Password updated successfully.'}, status=200)

# 更新个人资料
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Profile updated successfully'})
    return Response(serializer.errors, status=400)

# 查看订单历史
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_history(request):
    orders = Order.objects.filter(BuyerID=request.user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)