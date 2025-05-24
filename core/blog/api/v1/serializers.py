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

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), write_only=True
    )
    category_names = serializers.StringRelatedField(
        many=True, source="category", read_only=True
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "title",
            "content",
            "snippet",
            "category",
            "category_names",
            "status",
            "relative_url",
            "absolute_url",
            "published_at",
        ]
        read_only_fields = ["author"]

    def get_absolute_url(self, obj):
        request = self.context.get("request")
        url = obj.get_absolute_api_url()
        return request.build_absolute_uri(url) if request else url
