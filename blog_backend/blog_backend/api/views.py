from django.db.models import Prefetch

from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from blog_backend.blog.models import Post, Comment, Tag
from blog_backend.api.serializers import PostSerializer, CommentSerializer, TagSerializer
from blog_backend.api.permissions import PostPermissions, CommentPermissions


class PostViewSet(viewsets.ModelViewSet):
    # Source: https://stackoverflow.com/a/56869088
    queryset = Post.objects.prefetch_related(Prefetch('comments', Comment.objects.filter(approved=True)))
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, PostPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, PostPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    lookup_field = 'slug'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.filter(approved=True)
    permission_classes = [permissions.IsAuthenticated, CommentPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #permission_classes = [permissions.IsAuthenticated]
