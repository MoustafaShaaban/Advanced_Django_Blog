from graphql import GraphQLError

import graphene

from docker_blog_backend.blog.models import Post, Comment, Tag

from .types import (
    PostType,
    PostNode,
    CommentType,
)
from .inputs import TagInput



class CreatePostRelayMutation(graphene.relay.ClientIDMutation):

    class Input:
        title = graphene.String()
        tags = graphene.List(TagInput)
        content = graphene.String()

    success = graphene.Boolean()
    post = graphene.Field(PostNode)


    def mutate_and_get_payload(root, info, **input):
        success = True
        user = info.context.user
        tags = []

        for tag_input in input.get('tags'):
            tag = Tag.objects.get(slug=tag_input['slug'])
            if tag is None:
                return CreatePostRelayMutation(success=False, post=None)
            tags.append(tag)

        post_instance = Post.objects.create(
            title=input.get('title'),
            author=user,
            content=input.get('content'),
        )
        post_instance.save()
        post_instance.tag.set(tags)
        success = True
        return CreatePostRelayMutation(success=success, post=post_instance)


class UpdatePostRelayMutation(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.Int(required=True)
        title = graphene.String()
        tags = graphene.List(TagInput)
        content = graphene.String()

    success = graphene.Boolean()
    post = graphene.Field(PostNode)


    def mutate_and_get_payload(root, info, id, **input):
        success = True
        user = info.context.user
        tags = []
        post_instance = Post.objects.get(pk=id)

        if post_instance.author != user:
            raise GraphQLError("Only post author can update it")
        else:
            for tag_input in input.get('tags'):
                tag = Tag.objects.get(slug=tag_input.get('slug'))
                if tag is None:
                    return UpdatePostRelayMutation(success=False, post=None)
                tags.append(tag)

            post_instance.title = input.get('title')
            post_instance.content = input.get('content')
            post_instance.save()
            post_instance.tag.set(tags)
            success = True
        return UpdatePostRelayMutation(success=success, post=post_instance)


class DeletePostRelayMutation(graphene.relay.ClientIDMutation):

    class Input:
        id = graphene.Int()

    success = graphene.Boolean()

    def mutate_and_get_payload(root, info, id):
        user = info.context.user
        post_instance = Post.objects.get(pk=id)

        if not post_instance:
            raise GraphQLError("No post found with the provided id")

        if post_instance.author != user:
            raise GraphQLError("Only post author can delete it")
        else:
            post_instance.delete()
            success = True

        return DeletePostRelayMutation(success=success)



class CreateCommentRelayMutation(graphene.relay.ClientIDMutation):
    class Input:
        email = graphene.String()
        comment = graphene.String()
        #post_id = graphene.Int()
        post_slug = graphene.String()

    post = graphene.Field(PostType)
    comment = graphene.Field(CommentType)
    success = graphene.Boolean()


    def mutate_and_get_payload(self, info, **input):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to add a comment!')

        post = Post.objects.get(slug=input.get('post_slug'))
        if not post:
            raise GraphQLError('Invalid Post Slug!')

        comment = Comment.objects.create(
            user=user,
            post=post,
            email=input.get('email'),
            comment=input.get('comment'),
        )
        success = True

        return CreateCommentRelayMutation(comment=comment, success=success)


class UpdateCommentRelayMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.Int()
        comment = graphene.String()

    success = graphene.Boolean()
    comment = graphene.Field(CommentType)

    def mutate_and_get_payload(root, info, id, comment):
        success = False
        user = info.context.user
        comment_instance = Comment.objects.get(pk=id)

        if comment_instance.user != user:
            raise GraphQLError("Only comment user can update it")
        else:
            comment_instance.comment = comment
            comment_instance.save()
            success = True
        return UpdateCommentRelayMutation(success=success, comment=comment_instance)


class DeleteCommentRelayMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.Int(required=True)

    success = graphene.Boolean()

    @staticmethod
    def mutate_and_get_payload(root, info, id):
        user = info.context.user
        comment_instance = Comment.objects.get(pk=id)

        if comment_instance.user != user:
            raise GraphQLError("Only comment user can delete it")
        else:
            comment_instance.delete()
            success = True
        return DeleteCommentRelayMutation(success=success)
