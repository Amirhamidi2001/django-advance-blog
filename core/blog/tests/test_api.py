import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from blog.models import Category, Post
from accounts.models import CustomUser, UserProfile


@pytest.fixture
def user(db):
    user = CustomUser.objects.create_user(
        email="testuser@example.com", password="pass123"
    )
    return user


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def profile(user):
    return UserProfile.objects.get(user=user)


@pytest.fixture
def category():
    return Category.objects.create(name="Technology")


@pytest.fixture
def post(profile, category):
    post = Post.objects.create(
        title="Test Post",
        author=profile,
        content="Test content",
        status=True,
    )
    post.category.set([category])
    return post


# ------------------------------
#           TESTS
# ------------------------------


def test_create_post(auth_client, category):
    url = reverse("blog:api-v1:post-list")
    data = {
        "title": "New Post",
        "content": "New content",
        "category": [category.id],
        "status": True,
    }
    response = auth_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["title"] == "New Post"
    assert "snippet" in response.data


def test_list_posts(auth_client, post):
    url = reverse("blog:api-v1:post-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_items"] == 1
    assert response.data["results"][0]["title"] == post.title


def test_retrieve_post(auth_client, post):
    url = reverse("blog:api-v1:post-detail", args=[post.id])
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == post.title
    assert "content" in response.data
    assert "snippet" not in response.data


def test_update_post(auth_client, post):
    url = reverse("blog:api-v1:post-detail", args=[post.id])
    data = {"title": "Updated Post"}
    response = auth_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Updated Post"


def test_delete_post(auth_client, post):
    url = reverse("blog:api-v1:post-detail", args=[post.id])
    response = auth_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_create_category(auth_client):
    url = reverse("blog:api-v1:category-list")
    response = auth_client.post(url, {"name": "Science"})
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Science"


def test_list_categories(auth_client, category):
    url = reverse("blog:api-v1:category-list")
    response = auth_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["name"] == category.name
