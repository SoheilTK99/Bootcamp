from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils import timezone
from .models import OtpCode, validate_iran_phone
from rest_framework_simplejwt.tokens import RefreshToken





User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role", "phone", "gender")
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "phone", "gender")

class JWTObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["username"] = user.username
        return token





# OTP برای

User = get_user_model()

class OtpRequestSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[validate_iran_phone])

class OtpVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=11, validators=[validate_iran_phone])
    code  = serializers.CharField(max_length=6)

    def validate(self, attrs):
        phone = attrs["phone"]
        code  = attrs["code"]
        # آخرین OTP معتبر را پیدا کن
        qs = OtpCode.objects.filter(phone=phone).order_by("-created_at")
        otp = qs.first()
        if not otp:
            raise serializers.ValidationError({"code": "کدی ارسال نشده است."})
        if otp.is_expired():
            raise serializers.ValidationError({"code": "کد منقضی شده است."})
        # محدودسازی تعداد تلاش‌ها
        if otp.attempts >= 5:
            raise serializers.ValidationError({"code": "تلاش‌های بیش از حد. بعداً امتحان کنید."})
        # افزایش کانتر
        if otp.code != code:
            otp.attempts += 1
            otp.save(update_fields=["attempts"])
            raise serializers.ValidationError({"code": "کد نادرست است."})
        attrs["otp_obj"] = otp
        return attrs

    def create(self, validated_data):
        phone = validated_data["phone"]
        otp   = validated_data["otp_obj"]

        # اگر کاربر وجود نداشت بساز (ثبت‌نام با phone)
        user, created = User.objects.get_or_create(phone=phone, defaults={
            "username": f"user_{phone}",  # نام کاربری خودکار
            "role": User.Roles.END_USER,
            "is_active": True,
        })

        # OTP مصرف شود (حذف یا منقضی)
        otp.delete()

        # JWT تولید کن
        refresh = RefreshToken.for_user(user)
        # کلایم‌های اضافه
        refresh["role"] = user.role
        refresh["username"] = user.username

        return {
            "user": user,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


