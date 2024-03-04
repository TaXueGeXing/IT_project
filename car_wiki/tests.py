from django.test import TestCase
from .models import Car

class CarModelTestCase(TestCase):
    def setUp(self):
        # 在每个测试方法之前创建测试数据
        for i in range(5):
            Car.objects.create(
                Type="Test",
                Define="Test",
                Brand=str(i),
            )

    def test_car_objects_created(self):
        # 测试 Car 对象是否成功创建
        car_count = Car.objects.count()
        self.assertEqual(car_count, 5, "Expected 5 Car objects to be created")

    def test_car_object_attributes(self):
        # 测试 Car 对象的属性值
        all_cars = Car.objects.all()

        for car in all_cars:
            print(f"CarID: {car.CarID}, Type: {car.Type}, Define: {car.Define}, Brand: {car.Brand}")


# 使用以下命令运行测试
# python manage.py test your_app_name


# Create your tests here.
