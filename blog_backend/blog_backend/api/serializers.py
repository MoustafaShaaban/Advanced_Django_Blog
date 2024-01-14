from rest_framework import serializers
from django.contrib.auth import get_user_model

from blog_backend.blog.models import Post, Comment, Tag


class UserSerializer(serializers.ModelSerializer):
    # https://github.com/encode/django-rest-framework/issues/1984#issuecomment-60267220
    class Meta:
        model = get_user_model()
        fields = ('name', 'username', 'avatar',)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    # Set the user field explicitly to prevent the serializer from returning all the User Model fields
    author = UserSerializer(required=False)
    published_at = serializers.DateTimeField(required=False, format='%Y/%m/%d %H:%M')
    
    class Meta:
        model = Post
        depth = 1
        fields = ['title', 'author', 'slug', 'content', 'published_at', 'updated_at', 'tag']

        extra_kwargs = {
            'author': {'read_only': True},
            'url': {'lookup_field': 'slug'}
        }
        lookup_field = 'slug'

    def create(self, validated_data):
        tags_list = []
        tags_data = validated_data.get('tag')

        new_post = Post.objects.create(
            title=validated_data.get('title'),
            content=validated_data.get('content')
        )

        for tag_input in tags_data:
            tag_instance = Tag.objects.get(pk=tag.id)
            tags_list.append(tag_instance)

        new_post.save()
        new_post.tag.add(tags_list)

        return new_post


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'email', 'comment', 'user', 'post', 'published_at']
        extra_kwargs = {
            'user': {'read_only': True},
        }
