from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from blog.models import Post, Category
from .serializers import PostSerializer, CategorySerializer


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def post_list(request):
    """
    List all code posts or create a new post.
    """
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def post_detail(request, pk):
    """
    Retrieve, update, or delete a code post.
    """
    post = get_object_or_404(Post, pk=pk, status=True)

    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == "DELETE":
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class PostList(APIView):
#     """
#     View to list and create posts. Only authenticated users can create posts.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get(self, request):
#         """
#         List all posts that are active (status=True).
#         No authentication required for read access.
#         """
#         posts = Post.objects.filter(status=True)
#         serializer = self.serializer_class(posts, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         """
#         Create a new post. Only accessible by authenticated users.
#         """
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     """
#     Retrieve, update, or delete a Post instance.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer

#     def get(self, request, pk):
#         """Retrieve a specific Post instance by its primary key (pk)."""
#         post = get_object_or_404(Post, pk=pk, status=True)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         """Update an existing Post instance."""
#         post = get_object_or_404(Post, pk=pk, status=True)
#         serializer = self.serializer_class(post, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         """Delete a specific Post instance."""
#         post = get_object_or_404(Post, pk=pk, status=True)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


# class PostList(ListCreateAPIView):
#     """
#     API view for listing and creating posts.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=True)


# class PostDetail(RetrieveUpdateDestroyAPIView):
#     """
#     API view for retrieving, updating, and deleting individual posts.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=True)


# class PostViewSet(viewsets.ViewSet):
#     """
#     A viewset for handling CRUD operations for Post objects.
#     """

#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=True)

#     def list(self, request):
#         serializer = self.serializer_class(self.queryset, many=True)
#         return Response(serializer.data)

#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset, pk=pk)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk)
#         serializer = self.serializer_class(post, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def partial_update(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk)
#         serializer = self.serializer_class(post, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def destroy(self, request, pk=None):
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations for `Post` objects.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A viewset for handling CRUD operations for `Category` objects.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
