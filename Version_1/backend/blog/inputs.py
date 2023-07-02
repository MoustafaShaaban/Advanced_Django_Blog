import graphene

class TagInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    slug = graphene.String()

class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    tags = graphene.List(TagInput)
    content = graphene.String()