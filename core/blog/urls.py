from django.urls import path, include
from django.views.generic import TemplateView
from blog.views import (
    IndexView,
    PostListView,
    PostDetailView,
    ContactFormView,
    PostCreateView,
    PostEditView,
    PostDeleteView,
)

app_name = "blog"

urlpatterns = [
    path("", TemplateView.as_view(template_name="blog/index.html")),
    path("index/", IndexView.as_view(), name="index"),
    path("contact/", ContactFormView.as_view(), name="contact"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/create/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/edit/", PostEditView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
    path("api/v1/", include("blog.api.v1.urls")),
]
