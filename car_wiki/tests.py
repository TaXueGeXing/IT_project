from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Car, CarDetail


class CarCreateTestCase(TestCase):
    # Test car create
    def setUp(self):
        # Create five 5 objects
        for i in range(5):
            Car.objects.create(
                car_model="Test",
                car_brand=str(i),
            )

    def test_car_objects_created(self):
        # Test whether the Car object is successfully created
        car_count = Car.objects.count()
        self.assertEqual(car_count, 5, "Expected 5 Car objects to be created")


class CarDetailTestCase(TestCase):
    # Test car detail
    def setUp(self):
        # Create test data
        self.car1 = Car.objects.create(car_model='Test Model', car_brand='Test car_brand')
        self.car2 = Car.objects.create(car_model='Model', car_brand='car_brand')
        self.car_detail1 = CarDetail.objects.create(car=self.car1, define='Test Definition', picture='path/to/test_image1.jpg')
        self.car_detail2 = CarDetail.objects.create(car=self.car2, define='Test', picture='test_image4.jpg')

    def test_car_detail(self):
        # Assert relationship
        self.assertEqual(self.car_detail1.car, self.car1)
        self.assertEqual(self.car_detail2.car, self.car2)


class CarWikiTests(APITestCase):
    #  Car wiki test
    def setUp(self):
        # Create two objects
        self.car1 = Car.objects.create(car_model='Model1', car_brand='car_brand1')
        self.car2 = Car.objects.create(car_model='Model2', car_brand='car_brand2')
        # Create associated details for two cars
        CarDetail.objects.create(car=self.car1, define='Definition for Model1', picture='path/to/test_image1.jpg')
        CarDetail.objects.create(car=self.car2, define='Definition for Model2', picture='path/to/test_image2.jpg')

    def test_car_wiki_view(self):
        url = reverse('car_wiki')  # Get car wiki url
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        print("Response data:", response.data)  # Print response data for check


    def test_search_car_view(self):
        #  Search car test
        url = reverse('search_car')  # Get search car url
        response = self.client.get(url, {'car_brand': 'car_brand2', 'car_model': 'Model2'})  # Add search keywords
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Check if the car is found
        self.assertEqual(len(response.data), 3)
        print("Response data:", response.data)  # Print response data for check
        print("Matching cars:", response.data)  # Print matching data for check
        print(response.data.get('car_brand'))
        self.assertIsNot(response.data.get('car_brand'), 'car_brand1')  # Check if the car is correct
        self.assertEqual(response.data.get('car_model'), 'Model2')

    def test_car_detail_view(self):
        # Test car_detail_view
        url = reverse('car_detail', args=[self.car1.car_id])  # Create url for test car
        response = self.client.get(url)
        # Check if the page is found
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['car_model'], 'Model1')  # Check if the car is found

