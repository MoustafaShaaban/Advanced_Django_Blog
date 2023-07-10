from graphql import GraphQLError

import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from blog_backend.blog.models import Post, Comment, Tag
from blog_backend.blog.forms import TagForm

from .types import (
    PostType,
    PostNode,
    CommentType,
    TagType,
    UserType
)
from .inputs import PostInput, TagInput


class CreatePostMutation(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        user = info.context.user
        tags = []

        for tag_input in input.tags:
            tag = Tag.objects.get(slug=tag_input.slug)
            if tag is None:
                return CreatePostMutation(ok=False, post=None)
            tags.append(tag)
        
        post_instance = Post.objects.create(
            title=input.get('title'),
            author=user,
            content=input.get('content'),
        )
        post_instance.save()
        post_instance.tag.set(tags)
        return CreatePostMutation(ok=ok, post=post_instance)


class UpdatePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        user = info.context.user
        tags = []
        post_instance = Post.objects.get(pk=id)

        if post_instance.author != user:
            raise GraphQLError("Only post author can update it")
        else:
            for tag_input in input.tags:
                tag = Tag.objects.get(slug=tag_input.slug)
                if tag is None:
                    return CreatePostMutation(ok=False, post=None)
                tags.append(tag)

            post_instance.title = input.title
            post_instance.content = input.content
            post_instance.save()
            post_instance.tag.set(tags)
        return UpdatePostMutation(ok=ok, post=post_instance)

class DeletePostMutation(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = True
        user = info.context.user
        tags = []
        post_instance = Post.objects.get(pk=id)

        if post_instance.author != user:
            raise GraphQLError("Only post author can delete it")
        else:
            post_instance.delete()
        return DeletePostMutation(ok=ok)


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


class CreateCommentMutation(graphene.Mutation):
    user = graphene.Field(UserType)
    post = graphene.Field(PostType)

    class Arguments:
        post_id = graphene.Int()
        email = graphene.String()
        comment = graphene.String()

    def mutate(self, info, post_id, email, comment):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        post = Post.objects.filter(id=post_id).first()
        if not post:
            raise Exception('Invalid Link!')

        Comment.objects.create(
            user=user,
            post=post,
            email=email,
            comment=comment,
        )

        return CreateCommentMutation(user=user, post=post)


# class CreateCommentRelayMutation(graphene.relay.ClientIDMutation):
#     comment = graphene.Field(CommentNode)
#     post = graphene.Field(PostNode)
#     name = graphene.Field(UserType)

#     class Input:
#         email = graphene.String()
#         comment = graphene.String()
#         post = graphene.Int(required=True)

#     def mutate_and_get_payload(root, info, post_id, **kwargs):
#         name = info.context.user
#         if name.is_anonyomus:
#             raise GraphQLError('You must be logged in to comment!')

#         post = Post.objects.get(id=post_id)
#         if not post:
#             raise GraphQLError('Invaild post id!')

#         data = Comment(
#             post=post,
#             name=name,
#             email=kwargs.get('email'),
#             comment=kwargs.get('comment')
#         )

#         data.save()
#         return CreateCommentRelayMutation(data=data, name=name)


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