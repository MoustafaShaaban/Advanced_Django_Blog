import graphene

from .queries import Query

from .mutations import (
    CreatePostMutation,
    CreatePostRelayMutation,
    UpdatePostMutation,
    DeletePostMutation,
    CreateTagMutation,
    CreateCommentMutation,
    #CreateCommentRelayMutation,
    UpdateTagMutation,
    DeleteTagMutation
)


class Mutations(graphene.ObjectType):
    create_post = CreatePostMutation.Field()
    update_post = UpdatePostMutation.Field()
    delete_post = DeletePostMutation.Field()

    create_comment = CreateCommentMutation.Field()

    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
