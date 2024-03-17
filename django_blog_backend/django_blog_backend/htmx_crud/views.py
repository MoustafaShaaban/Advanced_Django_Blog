from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django_blog_backend.blog.models import Post, Comment, Tag

# Create your views here.
