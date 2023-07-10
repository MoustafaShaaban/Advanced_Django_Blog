import graphene

class TagInput(graphene.InputObjectType):
    name = graphene.String()
    slug = graphene.String()

class PostInput(graphene.InputObjectType):
    title = graphene.String()
    tags = graphene.List(TagInput)
    content = graphene.String()