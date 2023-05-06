from django.contrib.auth import get_user_model

from graphql import GraphQLError

import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation

from .models import Post, Comment, Tag
from .forms import CommentForm, TagForm



class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        exclude = ('password', 'email', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            'id': ['exact'],
            'title': ['exact', 'icontains', 'istartswith'],
            'author': ['exact'],
            'updated_at': ['exact'],
            'content': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node,)


class CommentNode(DjangoObjectType):

    class Meta:
        model = Comment
        interfaces = (relay.Node, )


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'slug', 'author', 'content', 'updated_at', 'comments', 'tag')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'email', 'comment')


class TagType(DjangoObjectType):
    class Meta:
        model = Tag