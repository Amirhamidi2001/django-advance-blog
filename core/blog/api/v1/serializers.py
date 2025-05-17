from rest_framework import serializers
from blog.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    """

    class Meta:
        model = Post
        fields = ["id", "title", "author", "status", "content", "category", "published_at"]
