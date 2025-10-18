from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class SupportUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role", "is_active")
        read_only_fields = ("id", "username", "email", "role")
