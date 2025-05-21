from rest_framework.routers import DefaultRouter
from .views import PostModelViewSet, CategoryModelViewSet

router = DefaultRouter()
router.register("posts", PostModelViewSet, basename="post")
router.register("categories", CategoryModelViewSet, basename="category")
urlpatterns = router.urls

# from django.urls import path, include
# from .views import post_list, post_detail
# from .views import PostList, PostDetail

# app_name = "api-v1"

# urlpatterns = [
#     path("", post_list, name="post-list"),
#     path("<int:pk>/", post_detail, name="post-detail"),
#     path("posts/", PostList.as_view(), name="post-list"),
#     path("post/<int:pk>/", PostDetail.as_view(), name="post-detail"),
# ]
