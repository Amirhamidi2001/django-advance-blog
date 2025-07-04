from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    RegistrationSerializer,
    UserSerializer,
    CustomTokenObtainPairSerializer,
)


class RegistrationApiView(generics.CreateAPIView):
    """
    API view to handle user registration.
    """

    serializer_class = RegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "User registered successfully."}, status=status.HTTP_201_CREATED
        )


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

        user_data = UserSerializer(user).data

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
