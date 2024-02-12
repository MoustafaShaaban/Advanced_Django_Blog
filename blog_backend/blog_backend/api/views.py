from django.db.models import Prefetch

from rest_framework import permissions, viewsets, generics
from rest_framework.exceptions import APIException
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from blog_backend.blog.models import Post, Comment, Tag
from blog_backend.api.serializers import PostSerializer, CommentSerializer, TagSerializer
from blog_backend.api.permissions import PostPermissions, CommentPermissions


class PostFilters(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    content = filters.CharFilter(field_name="content", lookup_expr="icontains")
    slug = filters.CharFilter(field_name="slug", lookup_expr="icontains")

    class Meta:
        model = Post
        fields = ['title', 'content', 'slug']


class PostViewSet(viewsets.ModelViewSet):
    # Source: https://stackoverflow.com/a/56869088
    queryset = Post.objects.prefetch_related(Prefetch('comments', Comment.objects.filter(approved=True)))
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, PostPermissions]
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['title', 'content']
    filter_backends = (DjangoFilterBackend,)
    filterset_class= PostFilters
    lookup_field = 'slug'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserPostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, PostPermissions]
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['title', 'content']
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


class SearchForPosts(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, PostPermissions]

    def get_queryset(self):
        title = self.request.query_params.get('title', None)
        limit = self.request.query_params.get('limit', 5)

        try:
            return Post.objects.filter(title__icontains=title)[:int(limit)]
        except Post.DoesNotExist:
            return APIException('No post found with the provided title')


