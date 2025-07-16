import pytest
import jwt
from django.conf import settings
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models.users import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
def test_user_registration():
    client = APIClient()
    url = reverse("accounts:api-v1:register")
    data = {
        "email": "testuser@example.com",
        "password": "StrongPass123!",
        "password1": "StrongPass123!",
    }
    response = client.post(url, data)
    assert response.status_code == 201
    assert CustomUser.objects.filter(email="testuser@example.com").exists()


@pytest.mark.django_db
def test_jwt_login_verified_user():
    user = CustomUser.objects.create_user(
        email="login@example.com", password="pass1234", is_verified=True
    )
    client = APIClient()
    url = reverse("accounts:api-v1:jwt-create")
    response = client.post(url, {"email": user.email, "password": "pass1234"})
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_get_user_profile():
    user = CustomUser.objects.create_user(
        email="profile@example.com", password="pass1234", is_verified=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("accounts:api-v1:user-profile")

    response = client.get(url)
    assert response.status_code == 200
    assert response.data["email"] == user.email


@pytest.mark.django_db
def test_update_user_profile():
    user = CustomUser.objects.create_user(
        email="update@example.com", password="pass1234", is_verified=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("accounts:api-v1:user-profile")
    data = {"first_name": "Alice", "last_name": "Smith", "bio": "Updated bio"}

    response = client.put(url, data)
    assert response.status_code == 200
    assert response.data["first_name"] == "Alice"
    assert response.data["bio"] == "Updated bio"


@pytest.mark.django_db
def test_change_password_success():
    user = CustomUser.objects.create_user(
        email="changepass@example.com", password="OldPass123", is_verified=True
    )
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("accounts:api-v1:change-password")
    data = {
        "old_password": "OldPass123",
        "new_password": "NewPass456!",
        "confirm_password": "NewPass456!",
    }

    response = client.put(url, data)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.check_password("NewPass456!")


@pytest.mark.django_db
def test_account_activation_success():
    user = CustomUser.objects.create_user(
        email="inactive@example.com", password="pass123", is_verified=False
    )
    token = jwt.encode({"user_id": user.id}, settings.SECRET_KEY, algorithm="HS256")
    client = APIClient()
    url = reverse("accounts:api-v1:activation-confirm", kwargs={"token": token})

    response = client.get(url)
    assert response.status_code == 200
    user.refresh_from_db()
    assert user.is_verified is True


@pytest.mark.django_db
def test_resend_activation_email():
    user = CustomUser.objects.create_user(
        email="resend@example.com", password="pass123", is_verified=False
    )
    client = APIClient()
    url = reverse("accounts:api-v1:activation-resend")
    response = client.post(url, {"email": user.email})
    assert response.status_code == 200
    assert "Activation email resent successfully" in response.data["details"]
