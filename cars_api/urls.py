from rest_framework import routers

from cars_api.views import CarViewSet

app_name = 'cars_api'

router = routers.SimpleRouter()
router.register(r'cars', CarViewSet)
urlpatterns = router.urls
