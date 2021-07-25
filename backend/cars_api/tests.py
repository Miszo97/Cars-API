# Create your tests here.
import json

from cars_api.models import Car, Rate
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CarViewSetTestCase(APITestCase):

    def test_car_already_exists_in_database(self):
        """
        Check if the HTTP_400_BAD_REQUEST status code is returned when the sent car already exists in database
        """

        make = "Tesla"
        model = "Model 3"
        url = reverse('cars_api:cars-list')

        Car.objects.create(make=make, model=model)

        response = self.client.post(
            url, {"make": make, "model": model}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_car_does_not_exist_in_NHTSA(self):
        """
        Check if the HTTP_400_BAD_REQUEST status code is returned if the sent car doesn't exist in NHTSA
        """

        make = "Ford"
        model = "Mustan"

        url = reverse('cars_api:cars-list')

        response = self.client.post(
            url, {"make": make, "model": model}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_new_valid_car(self):
        """
        Check if the HTTP_201_CREATED status code is returned
        if the received car exists in NHTSA
        and is not currently in a database
        """

        make = "Ford"
        model = "Mustang"

        url = reverse('cars_api:cars-list')

        response = self.client.post(
            url, {"make": make, "model": model}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bad_post_body(self):
        """
        Check if the HTTP_400_BAD_REQUEST status code is returned if the POST message doesn't contain neccessary fields
        """
        url = reverse('cars_api:cars-list')

        response1 = self.client.post(url, {"make": "Ford"}, format="json")

        response2 = self.client.post(url, {"model": "Mustang"}, format="json")

        response3 = self.client.post(url, format="json")

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_existing_car(self):

        Car.objects.create(make="BMW", model="M1")
        pk = 1

        url = reverse('cars_api:cars-detail', args=[pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Car.objects.filter(pk=pk).exists())

    def test_delete_non_existing_car(self):
        pk = 1

        url = reverse('cars_api:cars-detail', args=[pk])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RateViewTestCase(APITestCase):

    def test_rate_car(self):
        make = "Tesla"
        model = "Model 3"

        Car.objects.create(make=make, model=model)

        url = reverse('cars_api:rate')

        response = self.client.post(
            url, {"car_id": 1, "rating": 5}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_rate_with_incorrect_number(self):
        """
        Test if the view returns HTTP_400_BAD_REQUEST status code if rate is not integer from the range 1 to 5
        """

        make = "Tesla"
        model = "Model 3"

        Car.objects.create(make=make, model=model)

        url = reverse('cars_api:rate')

        response1 = self.client.post(
            url, {"car_id": 1, "rating": 10}, format="json"
        )
        response2 = self.client.post(
            url, {"car_id": 1, "rating": 3.5}, format="json"
        )

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rate_not_existing_car(self):
        """
        Test if the view returns HTTP_400_BAD_REQUEST status code if someone tries to send a not existing car
        """

        url = reverse('cars_api:rate')

        response1 = self.client.post(
            url, {"car_id": 1, "rating": 10}, format="json"
        )

        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

    def test_rating_increments_rate_number(self):

        make = "Tesla"
        model = "Model 3"

        car = Car.objects.create(make=make, model=model)

        car_rates_number_before = car.rates_number()

        url = reverse('cars_api:rate')

        self.client.post(
            url, {"car_id": 1, "rating": 5}, format="json"
        )

        car_rates_number_after = car.rates_number()

        self.assertTrue(car_rates_number_after - car_rates_number_before == 1)


class PopularViewTest(APITestCase):
    def test_two_most_popular_cars(self):
        """
        Tests if the view returns 2 most popular cars
        """

        def add_rates_to_car(car, rates):
            for r in rates:
                car.rates.add(Rate.objects.create(
                    rating=r, car_id=car))

        car1 = Car.objects.create(make="BMW", model="M1")
        car2 = Car.objects.create(make="BMW", model="M2")
        car3 = Car.objects.create(make="BMW", model="M3")
        car4 = Car.objects.create(make="BMW", model="M4")

        add_rates_to_car(car1, [])
        add_rates_to_car(car2, [1, 2, 4, 5])
        add_rates_to_car(car3, [1, 2, 3])
        add_rates_to_car(car4, [1, 2, 4, 5, 4])

        url = reverse('cars_api:popular')

        response = self.client.get(url)
        returned_cars = json.loads(response.content)

        first = {
            "make": "BMW",
            "id": 4,
            "model": "M4",
            "rates_number": 5,
        }
        second = {
            "make": "BMW",
            "id": 2,
            "model": "M2",
            "rates_number": 4
        }

        self.assertEqual(returned_cars[0], first)
        self.assertEqual(returned_cars[1], second)
