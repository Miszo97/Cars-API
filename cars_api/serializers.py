from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from cars_api.helpers import exists_in_nhtsa

from .models import Car, Rate


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    make = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)
    avg_rating = serializers.FloatField(required=False)
    rates_number = serializers.IntegerField(required=False)

    def __init__(self, *args, **kwargs):

        super(CarSerializer, self).__init__(*args, **kwargs)

        if 'avg_rating' not in self.context:
            self.fields.pop('avg_rating')

        if 'rates_number' not in self.context:
            self.fields.pop('rates_number')

    class Meta:
        validators = [
            UniqueTogetherValidator(
                queryset=Car.objects.all(),
                fields=['make', 'model'],
                message='This car already exists in the databse'
            )
        ]

    def validate(self, data):
        """
        Check if provided correct data and if the car exists
        """

        make = data['make']
        model = data['model']

        if not exists_in_nhtsa(make, model):
            raise serializers.ValidationError("Such car does not exist")

        return data

    def create(self, validated_data):
        return Car.objects.create(**validated_data)


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'

    def validate_rating(self, value):
        if not (value >= 1 and value <= 5):
            raise serializers.ValidationError(
                "Please provide an integer from the range 1 to 5")
        return value
