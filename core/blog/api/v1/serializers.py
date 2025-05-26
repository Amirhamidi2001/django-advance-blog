from rest_framework import serializers
from blog.models import Category, Post
from accounts.models import UserProfile


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

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.parser_context.get("kwargs").get("pk"):
            rep.pop("snippet", None)
            rep.pop("relative_url", None)
            rep.pop("absolute_url", None)
        else:
            rep.pop("content", None)
        return rep

    def create(self, validated_data):
        validated_data["author"] = UserProfile.objects.get(
            user__id=self.context.get("request").user.id
        )
        return super().create(validated_data)
