from rest_framework import serializers

from blog_backend.blog.models import Post, Comment, Tag


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'content', 'published_at', 'updated_at', 'tag']

        extra_kwargs = {
            'author': { 'read_only': True },
            'url': {'lookup_field': 'slug'}
        }
        lookup_field = 'slug'



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'email', 'comment', 'user', 'post', 'published_at']
        extra_kwargs = {
            'user': { 'read_only': True },
        }



class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']