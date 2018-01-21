"""Api rest framework urls."""

from django.conf.urls import url, include
from rest_framework import routers

from api.views import TodoViewSet

router = routers.DefaultRouter()
router.register(r'todos', TodoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
