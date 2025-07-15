from django.test import TestCase
from django.utils import timezone
from accounts.models import CustomUser
from blog.models import Post, Category


class CategoryModelTest(TestCase):

    def test_str_returns_name(self):
        category = Category.objects.create(name="Django")
        self.assertEqual(str(category), "Django")


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="author@example.com", password="pass"
        )
        cls.profile = cls.user.profile
        cls.category = Category.objects.create(name="Tech")
        cls.post = Post.objects.create(
            title="Test Post",
            author=cls.profile,
            content="This is the full content of the post.",
            status=True,
            published_at=timezone.now(),
        )
        cls.post.category.set([cls.category])

    def test_post_str_returns_title(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_get_snippet_returns_first_100_chars(self):
        snippet = self.post.get_snippet()
        self.assertEqual(snippet, "This is the full content of the post.")

    def test_get_absolute_api_url(self):
        url = self.post.get_absolute_api_url()
        self.assertIn(f"/api/v1/posts/{self.post.pk}", url)
