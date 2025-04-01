from django.contrib import admin
from blog.models import Category, Post


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing blog categories.
    """

    list_display = ("name",)
    search_fields = ("name",)


class PostAdmin(admin.ModelAdmin):
    """
    Admin interface for managing blog posts.
    """

    date_hierarchy = "created_at"
    list_display = ("title", "author", "created_at", "status", "published_at")
    list_filter = ("status", "author", "created_at", "published_at")
    search_fields = ("title", "content", "author__username")
    fields = (
        "image",
        "title",
        "content",
        "author",
        "category",
        "status",
        "published_at",
    )
    filter_horizontal = ("category",)
    empty_value_display = "-empty-"

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
