from rest_framework import serializers

from .models import Car, Rate


class CarSerializer(serializers.ModelSerializer):
    rates = serializers.StringRelatedField(many=True)

    class Meta:
        model = Car
        fields = ["id", "car_make", "model", "rates"]


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = ["id", "rate_number", "rated_car"]
