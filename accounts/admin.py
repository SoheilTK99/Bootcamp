from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User , SupportProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra", {"fields": ("role", "phone", "gender")}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_superuser")



@admin.register(SupportProfile)
class SupportProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "scopes")
    search_fields = ("user__username",)    