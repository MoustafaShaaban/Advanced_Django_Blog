from graphql import GraphQLError

import graphene
from graphene_django.forms.mutation import DjangoModelFormMutation

from blog_backend.blog.models import Post, Comment, Tag
from blog_backend.blog.forms import TagForm

from .types import (
    PostType,
    CommentType,
    TagType,
)
from .inputs import PostInput, CommentInput


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


class CreateCommentMutation(graphene.Mutation):
    class Arguments:
        inputs = CommentInput(required=True)

    post = graphene.Field(PostType)
    comment = graphene.Field(CommentType)
        

    def mutate(self, info, inputs=None):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged to add a comment!')

        post = Post.objects.filter(id=inputs.post_id).first()
        if not post:
            raise GraphQLError('Invalid Post Id!')

        Comment.objects.create(
            user=user,
            post=post,
            email=inputs.email,
            comment=inputs.comment,
        )

        return CreateCommentMutation(post=post)


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