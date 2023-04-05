import graphene
from graphene import Field

from graphene_django import DjangoObjectType
from graphene_django.forms.mutation import DjangoModelFormMutation

from .models import Tag
from .forms import TagForm


class TagType(DjangoObjectType):
    class Meta:
        model = Tag


class TagMutation(DjangoModelFormMutation):
    tag = Field(TagType)


