import graphene

from .queries import Query

from .mutations import (
    CreatePostMutation,
    CreatePostRelayMutation,
    CreateTagMutation,
    CreateCommentMutation,
    #CreateCommentRelayMutation,
    UpdateTagMutation,
    DeleteTagMutation
)


class Mutations(graphene.ObjectType):
    create_post = CreatePostMutation.Field()

    create_comment = CreateCommentMutation.Field()

    create_tag = CreateTagMutation.Field()
    update_tag = UpdateTagMutation.Field()
    delete_tag = DeleteTagMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
