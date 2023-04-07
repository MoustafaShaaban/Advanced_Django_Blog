import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Post, Comment, Tag


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


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'content', 'updated_at', 'comments', 'tag')


class CommentType(DjangoObjectType):
    class Meta:
        model = Comment
        fields = ('id', 'name', 'post')


class TagType(DjangoObjectType):
    class Meta:
        model = Tag
        fields = ('id', 'title')


class Query(ObjectType):

    all_posts = graphene.List(PostType)

    all_posts_with_filters = DjangoFilterConnectionField(PostNode)
    my_posts_with_filters = DjangoFilterConnectionField(PostNode)

    all_comments = graphene.List(CommentType)
    all_tags = graphene.List(TagType)

    post_by_title = graphene.Field(PostType, title=graphene.String(required=True))
    post_by_tag = graphene.Field(PostType, tag=graphene.String(required=True))

    def resolve_all_comments(root, info):
        return Comment.objects.select_related('post').filter(approved=True).all()

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


class CreateTagMutation(graphene.Mutation):

    class Arguments:
        title = graphene.String(required=True)

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(root, info, cls, title):
        tag = Tag(title=title)
        tag.save()
        return CreateTagMutation(tag=tag)


class UpdateTagMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
    
    tag = graphene.Field(TagType)

    @classmethod
    def mutate(root, info, cls, id, title):
        tag = Tag.objects.get(id=id)
        tag.title = title
        tag.save()

        return UpdateTagMutation(tag=tag)


class DeleteTagMutation(graphene.Mutation):

    class Arguments:
        id = graphene.ID()

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(root, info, cls, id):
        tag = Tag.objects.get(id=id)
        tag.delete()
        return DeleteTagMutation(tag=tag)


class Mutations(graphene.ObjectType):

    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)