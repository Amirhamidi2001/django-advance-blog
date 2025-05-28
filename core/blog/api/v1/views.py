from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from blog.models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from .permissions import IsOwnerOrReadOnly


# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def post_list(request):
#     """
#     List all code posts or create a new post.
#     """
#     if request.method == "GET":
#         posts = Post.objects.filter(status=True)
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# @api_view(["GET", "PUT", "DELETE"])
# @permission_classes([IsAuthenticated])
# def post_detail(request, pk):
#     """
#     Retrieve, update, or delete a code post.
#     """
#     post = get_object_or_404(Post, pk=pk, status=True)

#     if request.method == "GET":
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     elif request.method == "PUT":
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     elif request.method == "DELETE":
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class PostList(APIView):
#     """
#     A class-based API view for listing and creating posts
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get(self, request, format=None):
#         """
#         Retrieves a list of active posts.
#         """
#         posts = Post.objects.filter(status=True)
#         serializer = self.serializer_class(posts, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         """
#         Creates a new post if the data is valid.
#         """
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     """
#     A class-based API view for retrieving, updating, and deleting a specific post
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get_object(self, pk):
#         """
#         Retrieve a single post by its primary key (pk).
#         """
#         return get_object_or_404(Post, pk=pk, status=True)

#     def get(self, request, pk):
#         """
#         Retrieves the details of a specific post.
#         """
#         post = self.get_object(pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         """
#         Updates a specific post if the data is valid.
#         """
#         post = self.get_object(pk)
#         serializer = self.serializer_class(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def patch(self, request, pk):
#         """
#         Partially updates a specific post if the data is valid.
#         """
#         post = self.get_object(pk)
#         serializer = self.serializer_class(post, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     def delete(self, request, pk):
#         """
#         Deletes a specific post.
#         """
#         post = self.get_object(pk)
#         post.delete()
#         return Response(
#             {"detail": "Deleted successfully"}, status=status.HTTP_204_NO_CONTENT
#         )


# class PostList(ListCreateAPIView):
#     """
#     View for listing and creating posts.
#     """
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Post.objects.filter(status=True)


# class PostDetail(RetrieveUpdateDestroyAPIView):
#     """
#     View for retrieving, updating, and deleting a specific post.
#     """
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Post.objects.filter(status=True)


class PostModelViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing, retrieving, creating, updating, and deleting posts.
    """

    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_at"]


class CategoryModelViewSet(viewsets.ModelViewSet):
    """
    Viewset for listing, retrieving, creating, updating, and deleting categories.
    """

    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    queryset = Category.objects.all()
