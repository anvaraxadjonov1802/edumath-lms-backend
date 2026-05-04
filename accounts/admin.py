from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = (
        "id",
        "email",
        "full_name",
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
    )
    list_filter = (
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
    )
    search_fields = ("email", "full_name")
    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Shaxsiy ma’lumotlar", {"fields": ("full_name", "role")}),
        (
            "Ruxsatlar",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Email tasdiqlash",
            {
                "fields": (
                    "is_email_verified",
                    "verification_code",
                    "verification_code_created_at",
                )
            },
        ),
        ("Muhim sanalar", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "is_email_verified",
                ),
            },
        ),
    )