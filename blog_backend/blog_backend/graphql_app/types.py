from django.contrib.auth import get_user_model

from graphene import relay
from graphene_django.types import DjangoObjectType

from blog_backend.blog.models import Post, Comment, Tag


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'content', 'updated_at', 'comments', 'tag')

        filter_fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains', 'istartswith'],
            'author': ['exact'],
            'updated_at': ['exact'],
            'content': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class TagNode(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
        interfaces = (relay.Node,)


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'content', 'updated_at', 'comments', 'tag')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'email', 'comment')


"""class CommentNode(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'email', 'comment')
        interfaces = (relay.Node,)"""


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')
