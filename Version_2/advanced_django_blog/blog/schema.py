import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Post


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'content': ['exact', 'icontains', 'istartswith'],
            'author': ['exact']
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    post = relay.Node.Field(PostNode)
    all_posts = DjangoFilterConnectionField(PostNode)


schema = graphene.Schema(query=Query)
