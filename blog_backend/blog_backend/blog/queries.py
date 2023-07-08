from graphql import GraphQLError

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .models import Post, Comment, Tag
from .types import (
    PostType,
    PostNode,
    CommentType,
    TagType
)


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_title = graphene.Field(PostType, title=graphene.String(required=True))
    posts_by_author = graphene.List(PostType, author=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    all_posts_with_filters = DjangoFilterConnectionField(PostNode)
    my_posts_with_filters = DjangoFilterConnectionField(PostNode)

    all_comments = graphene.List(CommentType)
    comments_by_post = graphene.List(CommentType, post=graphene.String())
    all_tags = graphene.List(TagType)

    @classmethod
    def resolve_all_comments(cls, root, info):
        return Comment.objects.select_related('post').filter(approved=True).all()

    @classmethod
    def resolve_all_tags(cls, root, info):
        return Tag.objects.all()

    @classmethod
    def resolve_posts_by_author(cls, root, info, author):
        return (
            Post.objects.prefetch_related("tag")
            .select_related("author")
            .filter(author__username=author)
        )

    @classmethod
    def resolve_post_by_title(cls, root, info, title):
        try:
            return Post.objects.prefetch_related("tag").select_related("author").get(title=title)
        except Post.DoesNotExist:
            return GraphQLError('No post found with the provided title')

    @classmethod
    def resolve_posts_by_tag(cls, root, info, tag):
        try:
            return (
                Post.objects.prefetch_related("tag").select_related("author").filter(tag__name__iexact=tag)
            )
        except Post.DoesNotExist:
            return GraphQLError('No post found with the provided tag')

    @classmethod
    def resolve_comments_by_post(cls, root, info, post):
        try:
            return (
                Comment.objects.filter(post__title__iexact=post)
            )
        except Comment.DoesNotExist:
            return GraphQLError('No comments found in this post')

    @classmethod
    def resolve_all_posts(cls, root, info):
        return Post.objects.all()

    @classmethod
    def resolve_my_posts(cls, root, info):
        # context will reference to the Django request
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(author=info.context.user)