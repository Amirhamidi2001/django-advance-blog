from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from blog.models import Post, Category

User = get_user_model()


class BlogViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="Admin@gmail.com", password="Admin@1234"
        )
        cls.profile = cls.user.profile
        cls.category = Category.objects.create(name="Tech")
        cls.post = Post.objects.create(
            title="Test Post",
            content="Post content here.",
            author=cls.profile,
            status=True,
            published_at=timezone.now(),
        )
        cls.post.category.add(cls.category)

    def setUp(self):
        self.client.login(email="Admin@gmail.com", password="Admin@1234")

    def test_index_view_status_code(self):
        response = self.client.get(reverse("blog:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/index.html")

    def test_post_list_view_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("blog:post-list"))
        self.assertRedirects(
            response, f'/accounts/login/?next={reverse("blog:post-list")}'
        )

    def test_post_list_view_logged_in(self):
        response = self.client.get(reverse("blog:post-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("posts", response.context)

    def test_post_detail_view_requires_login(self):
        self.client.logout()
        response = self.client.get(
            reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_post_detail_view_logged_in(self):
        response = self.client.get(
            reverse("blog:post-detail", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_contact_form_view_get(self):
        response = self.client.get(reverse("blog:contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/contact.html")

    def test_contact_form_submission(self):
        response = self.client.post(
            reverse("blog:contact"),
            {"name": "John", "message": "Hello there!"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Your message has been sent successfully.")

    def test_post_create_view(self):
        response = self.client.post(
            reverse("blog:post-create"),
            {
                "title": "New Post",
                "status": True,
                "content": "Some content",
                "category": [self.category.pk],
                "published_at": timezone.now(),
            },
        )
        self.assertEqual(response.status_code, 302)

    def test_post_edit_view(self):
        response = self.client.post(
            reverse("blog:post-edit", kwargs={"pk": self.post.pk}),
            {
                "title": "Updated Title",
                "status": True,
                "content": "Updated content",
                "category": [self.category.pk],
                "published_at": self.post.published_at,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, "Updated Title")

    def test_post_delete_view(self):
        response = self.client.post(
            reverse("blog:post-delete", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())
