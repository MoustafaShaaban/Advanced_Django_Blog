import graphene

from blog_backend.graphql_app.queries import Query

from blog_backend.graphql_app.mutations import (
    CreatePostMutation,
    UpdatePostMutation,
    DeletePostMutation,
    CreateTagMutation,
    CreateCommentMutation,
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
