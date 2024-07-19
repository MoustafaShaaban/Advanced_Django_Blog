import graphene
from graphene import Int


class TagInput(graphene.InputObjectType):
    # name = graphene.String()
    slug = graphene.String()


class PostInput(graphene.InputObjectType):
    title = graphene.String()
    tags = graphene.List(Int)
    content = graphene.String()


class CommentInput(graphene.InputObjectType):
    comment = graphene.String()
    # post_id = graphene.Int()
    post_slug = graphene.String()
