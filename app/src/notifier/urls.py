from django.urls import path, include
from rest_framework import routers

from .views import ClientViewSet, MailingViewSet

router = routers.DefaultRouter()
router.register(r'client', ClientViewSet, basename='client')
router.register(r'mailing', MailingViewSet, basename='mailing')

urlpatterns = [
    path('', include(router.urls)),
]
