from rest_framework import generics, permissions, status
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, JWTObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.response import Response
from .serializers import OtpRequestSerializer, OtpVerifySerializer
from .models import OtpCode





User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_object(self):
        return self.request.user

class JWTObtainPairView(TokenObtainPairView):
    serializer_class = JWTObtainPairSerializer

TokenRefreshView = TokenRefreshView
TokenVerifyView = TokenVerifyView




# OTP برای

class OtpRequestView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OtpRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        otp = OtpCode.create_for_phone(phone, lifetime_seconds=120)
        # TODO: ارسال از طریق SMS. توسعه: کد را برمی‌گردانیم.
        return Response({"detail": "کد ارسال شد.", "dev_code": otp.code}, status=status.HTTP_201_CREATED)

class OtpVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = OtpVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        user = data.pop("user")
        return Response({
            "user": {"id": user.id, "username": user.username, "phone": user.phone, "role": user.role},
            **data
        }, status=status.HTTP_200_OK)

