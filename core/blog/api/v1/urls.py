from django.urls import path, include
from .views import post_list, post_detail


app_name = "api-v1"

urlpatterns = [
    path("", post_list, name="post-list"),
    path("<int:pk>/", post_detail, name="post-detail"),
]
