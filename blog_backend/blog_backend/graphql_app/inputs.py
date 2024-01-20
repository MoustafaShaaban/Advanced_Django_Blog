import graphene


class TagInput(graphene.InputObjectType):
    #name = graphene.String()
    slug = graphene.String()


class PostInput(graphene.InputObjectType):
    title = graphene.String()
    tags = graphene.List(TagInput)
    content = graphene.String()

class CommentInput(graphene.InputObjectType):
    email = graphene.String()
    comment = graphene.String()
    #post_id = graphene.Int()
    post_slug = graphene.String()
