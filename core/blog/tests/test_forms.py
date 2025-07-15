from django.test import TestCase
from django.utils import timezone
from blog.forms import ContactForm, PostForm
from blog.models import Category, Post
from accounts.models import CustomUser
from django.core.files.uploadedfile import SimpleUploadedFile


class ContactFormTest(TestCase):

    def test_valid_data(self):
        form = ContactForm(
            data={"name": "John Doe", "message": "This is a test message."}
        )
        self.assertTrue(form.is_valid())

    def test_missing_name(self):
        form = ContactForm(data={"name": "", "message": "Message without a name"})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)

    def test_missing_message(self):
        form = ContactForm(data={"name": "Jane", "message": ""})
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)


class PostFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create_user(
            email="author@example.com", password="pass"
        )
        cls.category = Category.objects.create(name="Django")

    def test_valid_post_form(self):
        image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )
        form_data = {
            "title": "Test Title",
            "status": True,
            "content": "Post content here...",
            "category": [self.category.pk],
            "published_at": timezone.now(),
        }
        form = PostForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        form = PostForm(
            data={
                "title": "",
                "status": True,
                "content": "Test content",
                "category": [self.category.pk],
                "published_at": timezone.now(),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_invalid_category(self):
        form = PostForm(
            data={
                "title": "Test",
                "status": True,
                "content": "Test content",
                "category": [999],
                "published_at": timezone.now(),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("category", form.errors)
