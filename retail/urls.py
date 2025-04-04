from django.urls import path, include
from .views import NetworkNodeViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'network', NetworkNodeViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]