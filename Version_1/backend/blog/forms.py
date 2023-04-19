from django import forms

from .models import Post, Comment, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['user', 'email', 'comment', 'post']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author'
        ]