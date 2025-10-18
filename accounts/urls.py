from django.urls import path
from .views import RegisterView, MeView, JWTObtainPairView, TokenRefreshView, TokenVerifyView, OtpRequestView, OtpVerifyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('me/', MeView.as_view(), name='me'),
    path('jwt/create/', JWTObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),
    path("otp/request/", OtpRequestView.as_view(), name="otp-request"),
    path("otp/verify/",  OtpVerifyView.as_view(),  name="otp-verify"),
]
