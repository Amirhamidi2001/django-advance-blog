from django.urls import path, include
from .views import PostViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

app_name = "api-v1"

router = DefaultRouter()
router.register("post", PostViewSet, basename="post")
router.register("category", CategoryViewSet, basename="category")
urlpatterns = router.urls

# urlpatterns = [
# path("posts/", post_list, name="post-list"),
# path("post/<int:pk>/", post_detail, name="post-detail"),
# path("posts/", PostList.as_view(), name="post-list"),
# path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
# ]
