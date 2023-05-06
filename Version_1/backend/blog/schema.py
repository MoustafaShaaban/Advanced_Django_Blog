from django.contrib.auth import get_user_model

from graphql import GraphQLError

import graphene
from graphene import relay, ObjectType
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation

from .models import Post, Comment, Tag
from .forms import CommentForm


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
        fields = ('id', 'name')


class Query(ObjectType):
    all_posts = graphene.List(PostType)
    post_by_title = graphene.Field(PostType, title=graphene.String(required=True))
    posts_by_author = graphene.List(PostType, author=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())

    all_posts_with_filters = DjangoFilterConnectionField(PostNode)
    my_posts_with_filters = DjangoFilterConnectionField(PostNode)

    all_comments = graphene.List(CommentType)
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
    def resolve_all_posts(cls, root, info):
        return Post.objects.all()

    @classmethod
    def resolve_my_posts(cls, root, info):
        # context will reference to the Django request
        if not info.context.user.is_authenticated:
            return Post.objects.none()
        else:
            return Post.objects.filter(author=info.context.user)


class CreatePostMutation(graphene.Mutation):
    id = graphene.Int()
    title = graphene.String(required=True)
    content = graphene.String(required=True)
    tag = graphene.String(required=True)
    author = graphene.Field(UserType)

    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        tag = graphene.ID(required=True)

    @classmethod
    def mutate(cls, root, info, title, content, tag):
        user = info.context.user
        if user.is_anonyomus:
            raise GraphQLError('You must be logged in to comment!')

        post = Post.objects.create(
            title=title,
            content=content,
            tag=tag,
            author = user
        )

        return CreatePostMutation(
            id=post.id,
            title=post.title,
            content=post.content,
            tag=post.tag,
            author=post.author,
        )


class CreatePostRelayMutation(graphene.relay.ClientIDMutation):
    post = graphene.Field(PostNode)

    class Input:
        title = graphene.String()
        content = graphene.String()
    #    tag = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user

        post = Post(
            title=input.get('title'),
            content=input.get('content'),
        #    tag=input.get('tag'),
            author=user
        )
        post.save()

        return CreatePostRelayMutation(post=post)


# class CreateCommentRelayMutation(graphene.relay.ClientIDMutation):
#     comment = graphene.Field(CommentNode)
#     post = graphene.Field(PostNode)

#     class Input:
#         email = graphene.String()
#         comment = graphene.String()
#         post = graphene.ID(required=True)

#     def mutate_and_get_payload(root, info, post_id, **input):
#         name = info.context.user
#         if name.is_anonyomus:
#             raise GraphQLError('You must be logged in to comment!')

#         post = Post.objects.filter(pk=post_id).first()
#         if not post:
#             raise GraphQLError('Invaild post id!')

#         data = Comment(
#             post=post,
#             name=name,
#             email=input.get('email'),
#             comment=input.get('comment')
#         )

#         data.save()
#         return CreateCommentRelayMutation(data=data)





class CreateCommentMutation(DjangoModelFormMutation):
    comment = graphene.Field(CommentType)

    class Meta:
        form_class = CommentForm


class CreateTagMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(cls, root, info, name):
        tag = Tag(name=name)
        tag.save()
        return CreateTagMutation(tag=tag)


class UpdateTagMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(cls, root, info, id, name):
        tag = Tag.objects.get(id=id)
        tag.name = name
        tag.save()

        return UpdateTagMutation(tag=tag)


class DeleteTagMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    tag = graphene.Field(TagType)

    @classmethod
    def mutate(cls, root, info, id):
        tag = Tag.objects.get(id=id)
        tag.delete()
        return DeleteTagMutation(tag=tag)


class Mutations(graphene.ObjectType):
    create_post = CreatePostRelayMutation.Field()

    create_comment = CreateCommentMutation.Field()

    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
