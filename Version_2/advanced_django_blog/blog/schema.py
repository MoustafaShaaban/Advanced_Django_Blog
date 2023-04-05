import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Post, Comment, Tag


class PostNode(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = ('id', 'title', 'author', 'content')
        interfaces = (relay.Node,)


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'comments', 'tag')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'post')


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class Query(ObjectType):
    all_posts = DjangoFilterConnectionField(PostNode)
    my_posts = DjangoFilterConnectionField(PostNode)

    all_comments = graphene.List(CommentType)
    all_tags = graphene.List(TagType)

    post_by_title = graphene.Field(PostType, title=graphene.String(required=True))
    post_by_tag = graphene.Field(PostType, tag=graphene.String(required=True))

    def resolve_all_comments(root, info):
        return Comment.objects.select_related('post').all()

    def resolve_all_tags(root, info):
        return Tag.objects.all()

    def resolve_post_by_title(root, info, title):
        try:
            return Post.objects.get(title=title)
        except Post.DoesNotExist:
            return None

    def resolve_post_by_tag(root, info, tag):
        try:
            return Post.objects.get(tag=tag)
        except Post.DoesNotExist:
            return None

    def resolve_all_posts(self, info):
        return Post.objects.all()

    def resolve_my_posts(self, info):
        # context will reference to the Django request
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(author=info.context.user)


schema = graphene.Schema(query=Query)
