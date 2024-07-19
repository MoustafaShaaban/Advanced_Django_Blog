from django import template
from django.shortcuts import render, get_object_or_404

from docker_blog_backend.blog.models import Post, Tag

register = template.Library()


@register.simple_tag(name='num_comments')
def num_comments(slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(approved=True)
    num_comments = comments.count()

    return num_comments
