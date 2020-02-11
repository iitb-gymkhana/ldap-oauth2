from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from .views import InternalViewset

router = DefaultRouter()
router.register('', InternalViewset, base_name='internal')

urlpatterns = [
    url('^api', include(router.urls, namespace='api')),
]
