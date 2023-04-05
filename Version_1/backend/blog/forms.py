from django import forms

from .models import Comment, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['email', 'comment']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title']