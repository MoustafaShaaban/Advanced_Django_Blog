from graphql import GraphQLError

import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from .models import Post, Comment, Tag
from .forms import CommentForm, TagForm

from .types import (
    PostType,
    PostNode,
    CommentType,
    CommentNode,
    TagType,
    UserType
)





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


class CreateTagMutation(DjangoModelFormMutation):
    tag = graphene.Field(TagType)

    class Meta:
        form_class = TagForm


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