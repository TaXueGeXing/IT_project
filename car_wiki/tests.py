from django.test import TestCase

from .models import Car, CarDetail, Image
class CarModelTestCase(TestCase):
    def setUp(self):
        # 在每个测试方法之前创建测试数据
        for i in range(5):
            Car.objects.create(
                CarModel="Test",
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
            print(f"CarID: {car.CarID}, Modal: {car.CarModel}, Brand: {car.Brand}")


# 照片测试代码
class CarDetailImageTestCase(TestCase):

    def setUp(self):
        # 创建测试数据
        self.car1 = Car.objects.create(CarModel='Test Model', Brand='Test Brand')
        self.car2 = Car.objects.create(CarModel='Model', Brand='Brand')
        self.car_detail1 = CarDetail.objects.create(Car=self.car1, Define='Test Definition')
        self.car_detail2 = CarDetail.objects.create(Car=self.car2, Define='Test')
        self.image1 = Image.objects.create(CarDetail=self.car_detail1, picture='path/to/test_image1.jpg')
        self.image2 = Image.objects.create(CarDetail=self.car_detail1, picture='path/to/test_image2.jpg')
        self.image3 = Image.objects.create(CarDetail=self.car_detail1, picture='path/to/test_image3.jpg')
        self.image4 = Image.objects.create(CarDetail=self.car_detail2, picture='test_image4.jpg')
        self.image5 = Image.objects.create(CarDetail=self.car_detail2, picture='path/to/test_image5.jpg')

    def test_car_detail_images(self):
        # 断言关系是否正确
        self.assertEqual(self.car1.car_detail, self.car_detail1)
        self.assertEqual(self.car_detail2.Car, self.car2)

        # 获取关联的照片列表
        images1 = self.car_detail1.images.all()
        images2 = self.car_detail2.images.all()

        # 断言照片数量是否正确
        self.assertEqual(images1.count(), 3)
        self.assertEqual(images2.count(), 2)
        expected_image_name = 'test_image4.jpg'
        self.assertEqual(images2.first().picture.name, expected_image_name)

        # 断言每个照片是否关联到正确的 CarDetail
        for image in images1:
            self.assertEqual(image.CarDetail, self.car_detail1)
            print(f"Image {image.id} CarDetail: {image.CarDetail}, Expected CarDetail: {self.car_detail1}")
        for image in images2:
            self.assertEqual(image.CarDetail, self.car_detail2)
            print(f"Image {image.id} CarDetail: {image.CarDetail}, Expected CarDetail: {self.car_detail2}")

from django.test import TestCase

from car_wiki.models import Car, CarDetail, Image

# 照片测试代码
class CarDetailImageTestCase(TestCase):

    def setUp(self):
        # 创建测试数据
        self.car1 = Car.objects.create(CarModel='Test Model', Brand='Test Brand')
        self.car2 = Car.objects.create(CarModel='Model', Brand='Brand')
        self.car_detail1 = CarDetail.objects.create(Car=self.car1, Define='Test Definition')
        self.car_detail2 = CarDetail.objects.create(Car=self.car2, Define='Test')
        self.image1 = Image.objects.create(CarDetail=self.car_detail1, picture='path/to/test_image1.jpg')
        self.image2 = Image.objects.create(CarDetail=self.car_detail1, picture='path/to/test_image2.jpg')
        self.image3 = Image.objects.create(CarDetail=self.car_detail1, picture='path/to/test_image3.jpg')
        self.image4 = Image.objects.create(CarDetail=self.car_detail2, picture='test_image4.jpg')
        self.image5 = Image.objects.create(CarDetail=self.car_detail2, picture='path/to/test_image5.jpg')

    def test_car_detail_images(self):
        # 断言关系是否正确
        self.assertEqual(self.car1.car_detail, self.car_detail1)
        self.assertEqual(self.car_detail2.Car, self.car2)

        # 获取关联的照片列表
        images1 = self.car_detail1.images.all()
        images2 = self.car_detail2.images.all()

        # 断言照片数量是否正确
        self.assertEqual(images1.count(), 3)
        self.assertEqual(images2.count(), 2)
        expected_image_name = 'test_image4.jpg'
        self.assertEqual(images2.first().picture.name, expected_image_name)

        # 断言每个照片是否关联到正确的 CarDetail
        for image in images1:
            self.assertEqual(image.CarDetail, self.car_detail1)
            print(f"Image {image.id} CarDetail: {image.CarDetail}, Expected CarDetail: {self.car_detail1}")
        for image in images2:
            self.assertEqual(image.CarDetail, self.car_detail2)
            print(f"Image {image.id} CarDetail: {image.CarDetail}, Expected CarDetail: {self.car_detail2}")
# Create your tests here.
