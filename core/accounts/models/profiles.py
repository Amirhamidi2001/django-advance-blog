from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .users import CustomUser


class UserProfile(models.Model):
    """
    Model to store additional user profile information.
    This includes fields such as bio, profile picture, location, and birth date.
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a profile for a new user when a CustomUser is created.
    This is triggered after a CustomUser instance is saved.
    """
    if created:
        UserProfile.objects.create(user=instance)
