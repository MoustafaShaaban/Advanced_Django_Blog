from django import forms

from docker_blog_backend.blog.models import Post, Comment, Tag


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'tag',)

        widgets = {
            'tag': forms.CheckboxSelectMultiple()
        }
