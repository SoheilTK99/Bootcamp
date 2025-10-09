from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    class Roles(models.TextChoices):
        END_USER = "END_USER" , "End User" 
        SUPPORT = "SUPPORT" , "Support Staff"

    role = models.CharField(max_length=30, choices=Roles.choices, default=Roles.END_USER)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"