from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    """

    password = serializers.CharField(max_length=255, write_only=True)
    password1 = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password1"):
            raise serializers.ValidationError({"detail": "Passwords do not match"})

        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying basic user information.
    """

    class Meta:
        model = User
        fields = ("id", "email")
