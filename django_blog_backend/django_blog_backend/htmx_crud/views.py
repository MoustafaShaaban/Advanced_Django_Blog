import json

from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test, login_required
from django_htmx.http import HttpResponseClientRedirect

from django_blog_backend.blog.models import Post, Comment, Tag
from .forms import PostForm
from django_blog_backend.blog.forms import CommentForm


def index(request):
    return render(request, 'htmx/index.html')


def post_list(request):
    posts = Post.objects.all()
    form = CommentForm()

    context = {
        'posts': posts,
        'form': form
    }
    return render(request, 'htmx/post_list.html', context)


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk)
    tags = post.tag.all()
    comments = post.comments.filter(approved=True).order_by('-published_at')
    form = CommentForm()

    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'form': form,
    }

    return render(request, 'htmx/post_detail.html', context)


@login_required
def add_post(request):
    user = request.user

    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = user
            post = form.save()

            return HttpResponse(
                status=204,
                headers= {
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": f"{ post.title } added."
                    })
                }
            )

    else:
        form = PostForm()

    return render(request, "htmx/post_form.html", {
        "form": form,
    })

@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.author != user:
        raise PermissionDenied

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": f"{ post.title } updated."
                    })
                }
            )

    else:
        form = PostForm(instance=post)

    return render(request, 'htmx/post_form.html', {
        'form': form,
        'post': post
    })


@ require_http_methods(['DELETE'])
def remove_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if post.author != user:
        raise PermissionDenied

    post.delete()
    messages.success(request, 'Post Added Successfully.')
    return redirect(reverse('htmx_crud:index'))

@login_required
def create_comment(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment_instance = form.save(commit=False)
            comment_instance.post = post
            comment_instance.user = request.user
            comment_instance.save()
            # messages.success(request, 'Thank you for commenting, Your comment is pending admin approval.')
            return HttpResponse(
                status=204,
                headers= {
                    'HX-Trigger': json.dumps({
                        "postListChanged": None,
                        "showMessage": f"Thank you for commenting, Your comment is pending admin approval."
                    })
                }
            )
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post
    }

    return render(request, 'htmx/comments/comment_form.html', context)


class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """ A view to update a specific post. """
    model = Comment
    fields = ['comment']
    template_name = 'htmx/comments/update_comment.html'
    success_url = reverse_lazy('htmx_crud:index')
    success_message = "Comment Updated Successfully"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """ A view to delete a specific post. """
    model = Comment
    template_name = 'htmx/comments/delete_comment.html'
    success_url = reverse_lazy('htmx_crud:index')
    success_message = "Comment Deleted Successfully"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


# @login_required
# def index(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post = form.save()
#             messages.success(request, 'Post Added Successfully.')
#             context = { 'post': post }
#             return render(request, 'htmx/index.html#post-item', context)

#     context = { 'form': PostForm(), 'posts': Post.objects.all() }
#     return render(request, 'htmx/index.html', context)



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


# def post_detail(request, pk):
#     """Show a single post with all its tags and comments."""
#     post = get_object_or_404(Post, id=pk)
#     tags = post.tag.all()
#     comments = post.comments.filter(approved=True).order_by('-published_at')
#     comment_form = CommentForm()

#     context = {
#         'post': post,
#         'tags': tags,
#         'comments': comments,
#         'comment_form': comment_form,
#     }

#     return render(request, 'htmx/post_detail.html', context)


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
