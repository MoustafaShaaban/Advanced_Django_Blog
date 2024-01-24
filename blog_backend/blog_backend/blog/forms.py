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
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(PostForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        kwargs['commit']=False
        obj = super(PostForm, self).save(*args, **kwargs)
        if self.request:
            obj.author = self.request.user
        obj.save()
        return  obj
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'tag'
        ]
