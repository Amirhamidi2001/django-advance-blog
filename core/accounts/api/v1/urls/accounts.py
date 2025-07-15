from django.urls import path

from ..views import (
    ChangePasswordView,
    CustomAuthToken,
    CustomDiscardAuthToken,
    CustomTokenObtainPairView,
    RegistrationApiView,
    ActivationApiView,
    ActivationResendApiView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # Registration & password
    path("register/", RegistrationApiView.as_view(), name="register"),
    path(
        "activation/confirm/<str:token>/",
        ActivationApiView.as_view(),
        name="activation-confirm",
    ),
    path(
        "activation/resend/",
        ActivationResendApiView.as_view(),
        name="activation-resend",
    ),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    # Token authentication
    path("token/login/", CustomAuthToken.as_view(), name="token-login"),
    path("token/logout/", CustomDiscardAuthToken.as_view(), name="token-logout"),
    # JWT authentication
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
]
