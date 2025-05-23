from django.db import models
from django.urls import reverse

# from django.contrib.auth import get_user_model
# User = get_user_model()


class Category(models.Model):
    """
    Represents a category for blog posts.
    """

    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        """Returns the string representation of the category name."""
        return self.name


class Post(models.Model):
    """
    Represents a blog post.
    """

    title = models.CharField(max_length=200)
    author = models.ForeignKey("accounts.UserProfile", on_delete=models.CASCADE)
    status = models.BooleanField(default=0)
    content = models.TextField()
    image = models.ImageField(null=True, blank=True)
    category = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """Returns the string representation of the post title."""
        return self.title

    def get_snippet(self):
        """Returns a short snippet of the post content."""
        return self.content[0:100]

    def get_absolute_api_url(self):
        """Returns the absolute URL for the API detail view of this post."""
        return reverse("blog:api-v1:post-detail", kwargs={"pk": self.pk})
