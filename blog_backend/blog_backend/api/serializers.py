from rest_framework import serializers

from blog_backend.blog.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['title', 'slug', 'author', 'content', 'published_at', 'updated_at', 'tag']

        extra_kwargs = {
            'author': { 'read_only': True },
            'url': {'lookup_field': 'slug'}
        }
        lookup_field = 'slug'