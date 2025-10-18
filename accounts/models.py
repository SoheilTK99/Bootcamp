from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField  


class User(AbstractUser):
    class Roles(models.TextChoices):
        END_USER = "END_USER" , "End User" 
        SUPPORT = "SUPPORT" , "Support Staff"

    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.END_USER)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
    





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