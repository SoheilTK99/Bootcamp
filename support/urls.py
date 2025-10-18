from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupportPingView, SupportUserViewSet

router = DefaultRouter()
router.register(r'users', SupportUserViewSet, basename='support-users')

urlpatterns = [
    path("ping/", SupportPingView.as_view(), name="support-ping"),
    path("", include(router.urls)),
]
