from django.test import TestCase
from django.core.exceptions import ValidationError
from accounts.models import CustomUser


class CustomUserModelTest(TestCase):

    def test_create_user(self):
        user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_verified)
        self.assertTrue(admin.is_active)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaisesMessage(ValueError, "The Email field must be set"):
            CustomUser.objects.create_user(email=None, password="pass")

    def test_user_str_returns_email(self):
        user = CustomUser.objects.create_user(
            email="string@example.com", password="testpass"
        )
        self.assertEqual(str(user), "string@example.com")
