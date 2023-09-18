from rest_framework import permissions, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from blog_backend.blog.models import Post, Comment, Tag
from blog_backend.api.serializers import PostSerializer, CommentSerializer, TagSerializer
from blog_backend.api.permissions import PostPermissions, CommentPermissions


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
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
    queryset = Comment.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CommentPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]