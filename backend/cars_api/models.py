from django.db import models
from django.db.models.aggregates import Avg


class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.make + " " + self.model

    def avg_rating(self):
        return self.rates.all().aggregate(Avg("rating"))["rating__avg"]

    def rates_number(self):
        return self.rates.count()


class Rate(models.Model):
    rating = models.PositiveIntegerField()
    car_id = models.ForeignKey(
        Car, related_name="rates", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rating) + " " + str(self.car_id)
