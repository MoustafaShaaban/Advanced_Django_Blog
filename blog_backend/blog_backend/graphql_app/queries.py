from django.db.models import Prefetch
from graphql import GraphQLError

import graphene
from graphene_django.filter import DjangoFilterConnectionField

from blog_backend.blog.models import Post, Comment, Tag
from blog_backend.graphql_app.types import (
    PostType,
    PostNode,
    CommentType,
    TagType
)


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    post_by_id = graphene.Field(PostType, id=graphene.Int(required=True))
    post_by_slug = graphene.Field(PostType, slug=graphene.String(required=True))
    post_by_title = graphene.List(PostType, title=graphene.String(required=True))
    posts_by_author = graphene.List(PostType, author=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    all_posts_with_filters = DjangoFilterConnectionField(PostNode)
    my_posts_with_filters = DjangoFilterConnectionField(PostNode)

    all_comments = graphene.List(CommentType, approved=graphene.Boolean())
    approved_comments = graphene.List(CommentType)
    comments_by_post = graphene.List(CommentType, postTitle=graphene.String())
    all_tags = graphene.List(TagType)

    @classmethod
    def resolve_post_by_id(cls, root, info, id):
        try:
            return Post.objects.get(pk=id)
        except Post.DoesNotExist:
            return GraphQLError('No note found with the provided id')

    @classmethod
    def resolve_post_by_slug(cls, root, info, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return GraphQLError('No post found with the provided slug')

    @classmethod
    def resolve_all_comments(cls, root, info):
        return Comment.objects.filter(approved=True)

    @classmethod
    def resolve_approved_comments(cls, root, info):
        return Comment.objects.filter(approved=True).all()

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
            return Post.objects.prefetch_related("tag").select_related("author").filter(title__contains=title)
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
    def resolve_comments_by_post(cls, root, info, postTitle):
        try:
            return (
                Comment.objects.filter(post__title__icontains=postTitle)
            )
        except Comment.DoesNotExist:
            return GraphQLError('No comments found in this post')

    @classmethod
    def resolve_all_posts(cls, root, info):
        # Source: https://stackoverflow.com/a/56869088
        return Post.objects.prefetch_related(Prefetch('comments', Comment.objects.filter(approved=True)))

    @classmethod
    def resolve_my_posts(cls, root, info):
        # context will reference to the Django request
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(author=info.context.user)
