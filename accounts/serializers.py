from django.contrib.auth import authenticate
from .email_utils import send_verification_email
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("id", "email", "full_name", "password")

    def validate_email(self, value):
        email = value.lower()

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Bu email oldin ro‘yxatdan o‘tgan")

        return email

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = User.objects.create_user(
            password=password,
            is_active=True,
            is_email_verified=False,
            **validated_data
        )

        code = user.generate_verification_code()

        send_verification_email(
            to_email=user.email,
            code=code,
            is_resend=False,
        )

        return user

class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

        if user.is_email_verified:
            raise serializers.ValidationError("Bu email allaqachon tasdiqlangan")

        if user.is_verification_code_expired():
            raise serializers.ValidationError("Tasdiqlash kodi eskirgan. Yangi kod so‘rang")

        if user.verification_code != code:
            raise serializers.ValidationError("Tasdiqlash kodi noto‘g‘ri")

        attrs["user"] = user
        return attrs

    def save(self):
        user = self.validated_data["user"]
        user.is_email_verified = True
        user.verification_code = ""
        user.save(update_fields=["is_email_verified", "verification_code"])
        return user


class ResendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        email = value.lower()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Foydalanuvchi topilmadi")

        if user.is_email_verified:
            raise serializers.ValidationError("Bu email allaqachon tasdiqlangan")

        self.user = user
        return email

    def save(self):
        code = self.user.generate_verification_code()

        send_verification_email(
            to_email=self.user.email,
            code=code,
            is_resend=True,
        )

        return self.user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email").lower()
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            raise serializers.ValidationError("Email yoki parol noto‘g‘ri")

        if not user.is_email_verified:
            raise serializers.ValidationError("Avval emailingizni tasdiqlang")

        attrs["user"] = user
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "role",
            "is_email_verified",
        )