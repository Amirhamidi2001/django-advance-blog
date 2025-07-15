from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser
from accounts.models.profiles import UserProfile
from datetime import date


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="john.doe@example.com", password="testpassword123"
        )

    def test_userprofile_created_automatically(self):
        """Test that a UserProfile is created automatically for a new user."""
        self.assertTrue(hasattr(self.user, "profile"))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_userprofile_str_returns_email(self):
        """Test that the __str__ method returns user's email."""
        profile = self.user.profile
        self.assertEqual(str(profile), "john.doe@example.com")

    def test_userprofile_fields(self):
        """Test setting and getting profile fields."""
        profile = self.user.profile
        profile.first_name = "John"
        profile.last_name = "Doe"
        profile.bio = "Just a test user."
        profile.birth_date = date(1990, 1, 1)
        profile.save()

        updated_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(updated_profile.first_name, "John")
        self.assertEqual(updated_profile.last_name, "Doe")
        self.assertEqual(updated_profile.bio, "Just a test user.")
        self.assertEqual(updated_profile.birth_date, date(1990, 1, 1))
