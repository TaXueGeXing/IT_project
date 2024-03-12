from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Car, CarDetail
from .serializers import CarSerializer


class car_modelTestCase(TestCase):
    # python manage.py test car_wiki.tests.car_modelTestCase

    def setUp(self):
        # 在每个测试方法之前创建测试数据
        for i in range(5):
            Car.objects.create(
                car_model="Test",
                car_brand=str(i),
            )

    def test_car_objects_created(self):
        # 测试 Car 对象是否成功创建
        car_count = Car.objects.count()
        self.assertEqual(car_count, 5, "Expected 5 Car objects to be created")

    def test_car_object_attributes(self):
        # 测试 Car 对象的属性值
        all_cars = Car.objects.all()

        for car in all_cars:
            print(f"CarID: {car.car_id}, Modal: {car.car_model}, car_brand: {car.car_brand}")


# 照片测试代码
class CarDetailImageTestCase(TestCase):
    # python manage.py test car_wiki.tests.CarDetailImageTestCase

    def setUp(self):
        # 创建测试数据
        self.car1 = Car.objects.create(car_model='Test Model', car_brand='Test car_brand')
        self.car2 = Car.objects.create(car_model='Model', car_brand='car_brand')
        self.car_detail1 = CarDetail.objects.create(car=self.car1, define='Test Definition', picture='path/to/test_image1.jpg')
        self.car_detail2 = CarDetail.objects.create(car=self.car2, define='Test', picture='test_image4.jpg')

    def test_car_detail_images(self):
        # 断言关系是否正确
        self.assertEqual(self.car_detail1.car, self.car1)
        self.assertEqual(self.car_detail2.car, self.car2)





class CarWikiAPITests(APITestCase):
    # python manage.py test car_wiki.tests.CarWikiAPITests.test_car_detail_view
    def setUp(self):
        self.car1 = Car.objects.create(car_model='Model1', car_brand='car_brand1')
        self.car2 = Car.objects.create(car_model='Model2', car_brand='car_brand2')
        # 为两辆车创建关联的 CarDetail
        CarDetail.objects.create(car=self.car1, define='Definition for Model1', picture='path/to/test_image1.jpg')
        CarDetail.objects.create(car=self.car2, define='Definition for Model2', picture='path/to/test_image2.jpg')

    def test_car_wiki_view(self):
        url = reverse('car_wiki')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # print("Response data:", response.data)
        # python manage.py test car_wiki.tests.CarWikiAPITests.test_car_wiki_view

    def test_search_car_view(self):
        url = reverse('search_car')
        response = self.client.get(url, {'car_brand': 'car_brand2', 'car_model': 'Model2'})
        print("Response data:", response.data)
        print("Matching cars:", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        print(response.data.get('car_brand'))
        self.assertIsNot(response.data.get('car_brand'), 'car_brand1')
        self.assertEqual(response.data.get('car_model'), 'Model2')
        # 我想看搜索出的car_detail_view

    def test_car_detail_view(self):
        # 测试 car_detail_view 视图
        url = reverse('car_detail', args=[self.car1.car_id])  # 根据你的实际 URL 配置进行替换
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_model'], 'Model1')

