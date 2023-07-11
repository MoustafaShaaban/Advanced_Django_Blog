import graphene


class PostInput(graphene.InputObjectType):
    title = graphene.String()
    tags = graphene.List(TagInput)
    content = graphene.String()

class CommentInput(graphene.InputObjectType):
    email = graphene.String()
    comment = graphene.String()
    post_id = graphene.Int()