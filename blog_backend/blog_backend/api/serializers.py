from rest_framework import serializers
from django.contrib.auth import get_user_model

from blog_backend.blog.models import Post, Comment, Tag


class UserSerializer(serializers.ModelSerializer):
    # https://github.com/encode/django-rest-framework/issues/1984#issuecomment-60267220
    class Meta:
        model = get_user_model()
        fields = ('name', 'username', 'avatar',)


class PostSerializer(serializers.ModelSerializer):
    # Set the user field explicitly to prevent the serializer from returning all the User Model fields
    author = UserSerializer()
    published_at = serializers.DateTimeField(format='%Y/%m/%d %H:%M')
    
    class Meta:
        model = Post
        depth = 1
        fields = ['title', 'author', 'slug', 'content', 'published_at', 'updated_at', 'tag']

        extra_kwargs = {
            'author': {'read_only': True},
            'url': {'lookup_field': 'slug'}
        }
        lookup_field = 'slug'


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'email', 'comment', 'user', 'post', 'published_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name', 'slug']
