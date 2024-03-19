from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test, login_required

from django_blog_backend.blog.models import Post, Comment, Tag
from .forms import PostForm

@login_required
def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post = form.save()
            messages.success(request, 'Post Added Successfully.')
            context = { 'post': post }
            return render(request, 'htmx/index.html#post-item', context)

    context = { 'form': PostForm(), 'posts': Post.objects.all() }
    return render(request, 'htmx/index.html', context)
