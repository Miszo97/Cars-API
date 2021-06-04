from rest_framework import serializers

from .models import Car, Rate


def car_exists_in_ntfs(make, model):
    return True


class CarSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    make = serializers.CharField(max_length=100)
    model = serializers.CharField(max_length=100)

    def validate(self, data):
        """
        Check if provided correct data and if the car exists
        """

        try:
            make = data['make']
            model = data['model']
        except KeyError:
            raise serializers.ValidationError(
                "the request post should contain make and model fields")

        if not car_exists_in_ntfs(make, model):
            raise serializers.ValidationError("Such car does not exist")

        return data

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def to_representation(self, instance):
        """ Add addictional fields """

        ret = super().to_representation(instance)

        if 'avg_rating' in self.context:
            ret['avg_rating'] = instance.average_rate()

        if 'rates_number' in self.context:
            ret['rates_number'] = instance.rates_number()

        return ret


class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate

    def validate_rate_number(self, value):
        if not (isinstance(value, int) and value >= 0 and value <= 5):
            raise serializers.ValidationError(
                "Please provide an integer from the range 0 to 5")
        return value
