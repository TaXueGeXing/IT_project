from django.shortcuts import render, redirect, get_object_or_404
from .models import Car, CarDetail


def car_wiki(request):
    return render(request, 'carwiki.html')


def carwiki_view(request):
    # 获取默认产品（最新发布的五种车）
    default_cars = Car.objects.filter(is_default=True).order_by('-create_time')[:5]
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
        brand = request.GET.get('Brand')
        car_model = request.GET.get('CarModel')

        # 处理搜索结果
        result_car = Car.objects.filter(
            # 根据实际情况调整筛选条件
            Brand__icontains=brand,
            CarModel__icontains=car_model,
        )
        if result_car.exists():
            car_id = result_car.first().carID
            return redirect('car_detail', car_id=car_id)

    else:
        result_car = None
    request.session['result_car'] = result_car
    return redirect('carwiki', result_car=result_car)


def car_detail(request, car_id):
    # 获取特定汽车的信息
    car_detail = get_object_or_404(CarDetail, carID=car_id)
    # 重定向到 car_detail 视图
    context = {'carDetail': car_detail}
    return render(request, 'car_detail.html', context)
