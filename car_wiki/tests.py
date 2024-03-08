from django.test import TestCase, override_settings, SimpleTestCase
from car_wiki.models import Car, CarDetail, Image
from .models import Car, CarDetail, Image
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework import status
from .models import Car, CarDetail, Image
from .serializers import CarSerializer


class car_modelTestCase(TestCase):
    def setUp(self):
        # 在每个测试方法之前创建测试数据
        for i in range(5):
            Car.objects.create(
                car_model="Test",
                car_car_brand=str(i),
            )

    def test_car_objects_created(self):
        # 测试 Car 对象是否成功创建
        car_count = Car.objects.count()
        self.assertEqual(car_count, 5, "Expected 5 Car objects to be created")

    def test_car_object_attributes(self):
        # 测试 Car 对象的属性值
        all_cars = Car.objects.all()

        for car in all_cars:
            print(f"CarID: {car.car_id}, Modal: {car.car_model}, car_brand: {car.car_car_brand}")


# 照片测试代码
class CarDetailImageTestCase(TestCase):

    def setUp(self):
        # 创建测试数据
        self.car1 = Car.objects.create(car_model='Test Model', car_brand='Test car_brand')
        self.car2 = Car.objects.create(car_model='Model', car_brand='car_brand')
        self.car_detail1 = CarDetail.objects.create(car=self.car1, define='Test Definition')
        self.car_detail2 = CarDetail.objects.create(car=self.car2, define='Test')
        self.image1 = Image.objects.create(car_detail=self.car_detail1, picture='path/to/test_image1.jpg')
        self.image2 = Image.objects.create(car_detail=self.car_detail1, picture='path/to/test_image2.jpg')
        self.image3 = Image.objects.create(car_detail=self.car_detail1, picture='path/to/test_image3.jpg')
        self.image4 = Image.objects.create(car_detail=self.car_detail2, picture='test_image4.jpg')
        self.image5 = Image.objects.create(car_detail=self.car_detail2, picture='path/to/test_image5.jpg')

    def test_car_detail_images(self):
        # 断言关系是否正确

        self.assertEqual(self.car_detail1.car, self.car1)
        self.assertEqual(self.car_detail2.car, self.car2)
        self.assertEqual(self.car2.Car, self.car2)
        # 获取关联的照片列表
        images1 = self.car1.images.all()
        images2 = self.car2.images.all()

        # 断言照片数量是否正确
        self.assertEqual(images1.count(), 3)
        self.assertEqual(images2.count(), 2)
        expected_image_name = 'test_image4.jpg'
        self.assertEqual(images2.first().picture.name, expected_image_name)

        # 断言每个照片是否关联到正确的 CarDetail
        for image in images1:
            self.assertEqual(image.CarDetail, self.car1)
            print(f"Image {image.id} CarDetail: {image.CarDetail}, Expected CarDetail: {self.car1}")
        for image in images2:
            self.assertEqual(image.CarDetail, self.car2)
            print(f"Image {image.id} CarDetail: {image.CarDetail}, Expected CarDetail: {self.car2}")




class CarWikiAPITests(APITestCase):
    def setUp(self):
        # 在每个测试方法运行前执行的设置
        self.car1 = Car.objects.create(car_model='Model1', car_brand='car_brand1')
        self.car2 = Car.objects.create(car_model='Model2', car_brand='car_brand2')


    def test_car_wiki_view(self):
        # 测试 car_wiki 视图
        url = reverse('car_wiki')  # 根据你的实际 URL 配置进行替换
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 根据你的测试数据进行调整

    def test_search_car_view(self):
        # 测试 search_car 视图
        url = reverse('search_car')  # 根据你的实际 URL 配置进行替换
        response = self.client.get(url, {'car_brand': 'car_brand1', 'car_model': 'Model1'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_brand'], 'car_brand1')

    def test_car_detail_view(self):
        # 测试 car_detail_view 视图
        url = reverse('car_detail', args=[self.car1.car_id])  # 根据你的实际 URL 配置进行替换
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_model'], 'Model1')
