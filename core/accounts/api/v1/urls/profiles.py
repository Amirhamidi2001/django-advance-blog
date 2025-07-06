from django.urls import path

from ..views import UserProfileDetailView


urlpatterns = [
    path("", UserProfileDetailView.as_view(), name="user-profile"),
]
