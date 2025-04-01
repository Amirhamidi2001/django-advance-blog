from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


# Customize the CustomUser admin interface
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # Define the fields to be displayed in the admin
    list_display = ("email", "is_staff", "is_active", "last_login")
    list_filter = ("is_staff", "is_active", "date_joined")
    search_fields = ("email",)
    ordering = ("email",)

    # Define the fields for creating and updating users
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important Dates", {"fields": ("last_login",)}),  # Removed 'date_joined' here
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    # Set the field to be used as the USERNAME_FIELD
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]


# Customize the UserProfile admin interface
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = (
        "user",
        "first_name",
        "last_name",
        "bio",
        "birth_date",
        "profile_picture",
    )
    search_fields = ("user__email", "first_name", "last_name")
    list_filter = ("birth_date",)


# Register the CustomUser, UserProfile model
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CustomUser, CustomUserAdmin)

