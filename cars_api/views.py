# Create your views here.

from django.db.models.aggregates import Count
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from cars_api.models import Car
from cars_api.serializers import CarSerializer, RateSerializer


class CarViewSet(mixins.DestroyModelMixin, viewsets.GenericViewSet):
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def list(self, request):
        ser = self.serializer_class(
            self.get_queryset(), many=True, context={'avg_rating': True})
        return Response(ser.data)

    def create(self, request):
        ser = CarSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


class RateView(generics.CreateAPIView):
    serializer_class = RateSerializer


class PopularView(APIView):
    def get(self, request):
        n_most_pulular_cars = Car.objects.annotate(num_rates=Count("rates")).order_by(
            "-num_rates"
        )[:2]
        ser = CarSerializer(n_most_pulular_cars, many=True,
                            context={'rates_number': True})
        return Response(ser.data, status=status.HTTP_200_OK)
