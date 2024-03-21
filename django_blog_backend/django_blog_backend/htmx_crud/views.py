from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test, login_required
from django_htmx.http import HttpResponseClientRedirect

from django_blog_backend.blog.models import Post, Comment, Tag
from .forms import PostForm
from django_blog_backend.blog.forms import CommentForm

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



# @login_required
# @require_http_methods(['DELETE'])
# def delete_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.author == request.user:
#         post.delete()
#     else:
#         raise Exception('You do not have permission to delete this post')

#     posts = Post.objects.all()

#     return render(request, 'htmx/index.html', { 'form': PostForm(), 'posts': posts})


def post_detail(request, pk):
    """Show a single post with all its tags and comments."""
    post = get_object_or_404(Post, id=pk)
    tags = post.tag.all()
    comments = post.comments.filter(approved=True).order_by('-published_at')
    comment_form = CommentForm()

    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'comment_form': comment_form,
    }

    return render(request, 'htmx/post_detail.html', context)


class HTMXUpdatePostView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """ A view to update a specific post. """
    model = Post
    fields = ['title', 'content', 'tag']
    template_name = 'htmx/update_post.html'
    success_url = reverse_lazy('htmx_crud:index')
    success_message = "Post Updated Successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """ A view to delete a specific post. """
    model = Post
    template_name = 'htmx/post_detail.html'
    success_message = "Post Deleted Successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseClientRedirect("/htmx_crud/")
