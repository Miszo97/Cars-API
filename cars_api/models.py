from django.db import models
from django.db.models.aggregates import Avg


class Car(models.Model):
    car_make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    def __str__(self):
        return self.car_make + " " + self.model

    def average_rate(self):
        return self.rates.all().aggregate(Avg("rate_number"))["rate_number__avg"]

    def rates_number(self):
        return self.rates.count()


class Rate(models.Model):
    rate_number = models.PositiveIntegerField()
    rated_car = models.ForeignKey(
        Car, related_name="rates", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.rate_number) + " " + str(self.rated_car)
