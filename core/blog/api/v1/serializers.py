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

    author = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)
    snippet = serializers.ReadOnlyField()
    get_absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "author", "status", "content", "snippet", "image",
            "category", "created_at", "updated_at", "published_at", "get_absolute_url"
        ]

    def get_get_absolute_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url()) if request else obj.get_absolute_url()
