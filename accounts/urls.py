from django.urls import path

from .views import (
    LoginView,
    ProfileView,
    RegisterView,
    ResendVerificationCodeView,
    VerifyEmailView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("resend-code/", ResendVerificationCodeView.as_view(), name="resend-code"),
    path("login/", LoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
]