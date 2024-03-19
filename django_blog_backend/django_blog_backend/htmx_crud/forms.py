from django import forms

from django_blog_backend.blog.models import Post, Comment, Tag


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'tag',)
