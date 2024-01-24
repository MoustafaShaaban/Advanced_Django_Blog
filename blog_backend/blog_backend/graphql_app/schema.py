import graphene

from blog_backend.graphql_app.queries import Query

from blog_backend.graphql_app.mutations import (
    CreatePostMutation,
    UpdatePostMutation,
    DeletePostMutation,

    CreateCommentMutation,
    UpdateCommentMutation,
    DeleteCommentMutation,

    CreateTagMutation,
    UpdateTagMutation,
    DeleteTagMutation
)

from blog_backend.graphql_app.relay_mutations import (
    CreatePostRelayMutation,
    UpdatePostRelayMutation,
    DeletePostRelayMutation,

    CreateCommentRelayMutation,
    UpdateCommentRelayMutation,
    DeleteCommentRelayMutation,
)


class Mutations(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    create_post_relay = CreatePostRelayMutation.Field()

    update_post = UpdatePostMutation.Field()
    update_post_relay = UpdatePostRelayMutation.Field()

    delete_post = DeletePostMutation.Field()
    delete_post_relay = DeletePostRelayMutation.Field()

    create_comment = CreateCommentMutation.Field()
    create_comment_relay = CreateCommentRelayMutation.Field()

    update_comment = UpdateCommentMutation.Field()
    update_comment_relay = UpdateCommentRelayMutation.Field()

    delete_comment = DeleteCommentMutation.Field()
    delete_comment_relay = DeleteCommentRelayMutation.Field()

    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
