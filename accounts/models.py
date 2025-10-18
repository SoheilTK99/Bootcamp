from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField  
from django.core.exceptions import ValidationError
import re
import secrets
from django.utils import timezone



# ---------- Phone validator ----------
phone_re = re.compile(r"^09\d{9}$")  # مثال ایران: 11 رقم و شروع با 09

def validate_iran_phone(value: str):
    # اگر فیلد اختیاری باشد، None/"" را رد نکنیم
    if value and not phone_re.match(value):
        raise ValidationError("شماره موبایل نامعتبر است. مثال: 09123456789")


# ---------- User ----------
class User(AbstractUser):
    class Roles(models.TextChoices):
        END_USER = "END_USER", "End User"
        SUPPORT  = "SUPPORT", "Support Staff"

    role   = models.CharField(max_length=20, choices=Roles.choices, default=Roles.END_USER)
    phone  = models.CharField(max_length=11, unique=True, null=True, blank=True,
                              validators=[validate_iran_phone])
    gender = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    



# برای دسترسی های پشتیبانی

SUPPORT_SCOPES = (
    ("users.read", "Read users"),
    ("users.write", "Write users"),
    ("users.delete", "Delete users"),
)

class SupportProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="support_profile")
    scopes = ArrayField(models.CharField(max_length=32, choices=SUPPORT_SCOPES), default=list, blank=True)

    def __str__(self):
        return f"SupportProfile<{self.user.username}>"
    

# ---------- OTP ----------
class OtpCode(models.Model):
    phone = models.CharField(max_length=11, db_index=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        indexes = [models.Index(fields=["phone", "expires_at"])]

    @staticmethod
    def generate_code():
        return f"{secrets.randbelow(10**6):06d}"

    @classmethod
    def create_for_phone(cls, phone: str, lifetime_seconds: int = 120):
        now = timezone.now()
        return cls.objects.create(
            phone=phone,
            code=cls.generate_code(),
            expires_at=now + timezone.timedelta(seconds=lifetime_seconds),
        )

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"OTP<{self.phone}:{self.code}>"
