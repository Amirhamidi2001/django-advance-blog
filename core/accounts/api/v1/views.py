from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from mail_templated import EmailMessage

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from jwt import decode
from jwt.exceptions import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
)

from ...models import UserProfile
from ..utils import EmailThread
from .serializers import (
    ActivationResendSerializer,
    ChangePasswordSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    RegistrationSerializer,
    UserProfileSerializer,
)

User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    """
    This view handles user registration requests, creates a user account
    """

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            email = serializer.validated_data["email"]
            user_obj = get_object_or_404(User, email=email)
            tokens = self.get_tokens_for_user(user_obj)
            try:
                email_obj = EmailMessage(
                    "email/activation_email.tpl",
                    {"token": tokens["access"]},
                    "Admin@gmail.com",
                    to=[email],
                )
                EmailThread(email_obj).start()
            except Exception as e:
                logger.error(f"Email send failed: {e}")
            return Response({"email": email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save()

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class CustomAuthToken(ObtainAuthToken):
    """
    Custom authentication view that returns user details along with token.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        user_data = CustomAuthTokenSerializer(user).data

        return Response({"token": token.key, "user": user_data})


class CustomDiscardAuthToken(APIView):
    """
    API view to handle user logout by deleting the user's auth token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View for obtaining JWT token pairs using a custom serializer.
    """

    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(generics.GenericAPIView):
    """
    API endpoint for allowing authenticated users to change their password.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(old_password):
                return Response(
                    {"old_password": ["Incorrect password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"detail": "Password updated successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's profile.
    """

    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj


class ActivationApiView(APIView):
    """
    API view for account activation via JWT token.
    """

    def get(self, request, token, *args, **kwargs):
        try:
            payload = decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if not user_id:
                return Response(
                    {"details": "Invalid token payload"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ExpiredSignatureError:
            return Response(
                {"details": "Token has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Invalid token signature"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (DecodeError, InvalidTokenError):
            return Response(
                {"details": "Invalid or malformed token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user_obj = get_object_or_404(User, pk=user_id)

        if user_obj.is_verified:
            return Response(
                {"details": "Your account is already verified."},
                status=status.HTTP_200_OK,
            )

        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "Your account has been verified and activated successfully."},
            status=status.HTTP_200_OK,
        )


class ActivationResendApiView(generics.GenericAPIView):
    """
    API view to handle resending of account activation emails.
    """

    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_obj = serializer.get_user()
        token = self.get_tokens_for_user(user_obj)

        try:
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "Admin@gmail.com",
                to=[user_obj.email],
            )
            EmailThread(email_obj).start()
        except Exception as e:
            logger.error(f"Failed to send activation email: {e}")
            return Response(
                {"details": "Failed to send activation email"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {"details": "Activation email resent successfully"},
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
