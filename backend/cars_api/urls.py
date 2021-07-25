from cars_api.views import CarViewSet, PopularView, RateView
from django.urls import path
from rest_framework import routers

app_name = 'cars_api'

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'cars', CarViewSet, basename='cars')

urlpatterns = [
    path('rate', RateView.as_view(), name='rate'),
    path('popular', PopularView.as_view(), name='popular'),
]

urlpatterns += router.urls
