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

from docker_blog_backend.blog.models import Post, Comment, Tag
from .forms import PostForm
from docker_blog_backend.blog.forms import CommentForm



class HomePage(generic.ListView):
    """Home page that shows all  blog posts with a maximum number of 5 posts per each page."""
    model = Post
    template_name = 'htmx/index.html'
    context_object_name = 'posts'
    paginate_by = 5


def post_detail(request, pk):
    """A view to return a single blog post by it's primary key and a form to add a comment"""
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



class HTMXCreatePostView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """ A view to create a new post. """
    model = Post
    fields = ['title', 'content', 'tag']
    template_name = 'htmx/htmx_create_post.html'
    success_url = reverse_lazy('htmx_crud:index')
    success_message = "Post Added Successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class HTMXUpdatePostView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """ A view to update a blog post by it's primary key. """
    model = Post
    fields = ['title', 'content', 'tag']
    template_name = 'htmx/htmx_update_post.html'
    #success_url = reverse_lazy('htmx_crud:index')
    success_message = "Post Updated Successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse('htmx_crud:post-detail', kwargs={'pk': self.object.pk})


class HTMXDeletePostView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """ A view to delete a blog post by it's primary key. """
    model = Post
    template_name = 'htmx/htmx_delete_post.html'
    success_url = reverse_lazy('htmx_crud:index')
    success_message = "Post Deleted Successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False



class HTMXCreateCommentView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """ A view to add a new comment to a blog post. """
    model = Comment
    fields = ['comment']
    template_name = 'htmx/comments/comment_form.html'
    # success_url = reverse_lazy('htmx_crud:index')
    success_message = "Thank you for commenting, Your comment is pending admin approval."

    def form_valid(self, form):
        # post = get_object_or_404(Post, id=pk)
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('htmx_crud:post-detail', kwargs={'pk': self.object.post.pk})


class HTMXUpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """ A view to update a comment by it's primary key. """
    model = Comment
    fields = ['comment']
    template_name = 'htmx/comments/update_comment.html'
    # success_url = reverse_lazy('htmx_crud:index')
    success_message = "Comment Updated Successfully"


    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_success_url(self):
        return reverse("htmx_crud:post-detail", kwargs={"pk": self.object.post.pk})


class HTMXDeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """ A view to delete a comment by it's primary key. """
    model = Comment
    template_name = 'htmx/comments/delete_comment.html'
    # success_url = reverse_lazy('htmx_crud:index')
    success_message = "Comment Deleted Successfully"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_success_url(self):
        return reverse('htmx_crud:post-detail', kwargs={'pk': self.object.post.pk})


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


# def index(request):
#     return render(request, 'htmx/index.html')


# def post_list(request):
#     posts = Post.objects.all()
#     form = CommentForm()

#     context = {
#         'posts': posts,
#         'form': form
#     }
#     return render(request, 'htmx/post_list.html', context)


# @login_required
# def add_post(request):
#     user = request.user

#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = user
#             post = form.save()
#             messages.success(request, 'Post Added Successfully.')
#             return HttpResponse(
#                 status=204,
#                 headers= {
#                     'HX-Trigger': json.dumps({
#                         "postListChanged": None,
#                         "showMessage": f"{ post.title } added."
#                     })
#                 }
#             )

#     else:
#         form = PostForm()

#     return render(request, "htmx/post_form.html", {
#         "form": form,
#     })

# @login_required
# def edit_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     user = request.user

#     if post.author != user:
#         raise PermissionDenied

#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)

#         if form.is_valid():

#             form.save()
#             return HttpResponse(
#                 status=204,
#                 headers={
#                     'HX-Trigger': json.dumps({
#                         "postListChanged": None,
#                         "showMessage": f"{ post.title } updated."
#                     })
#                 }
#             )

#     else:
#         form = PostForm(instance=post)

#     return render(request, 'htmx/post_form.html', {
#         'form': form,
#         'post': post
#     })


# @ require_http_methods(['DELETE'])
# def remove_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     user = request.user

#     if post.author != user:
#         raise PermissionDenied

#     post.delete()
#     messages.success(request, 'Post Deleted Successfully.')
#     return redirect(reverse_lazy('htmx_crud:index'))


# @login_required
# def create_comment(request, pk):
#     post = get_object_or_404(Post, id=pk)

#     if request.method == 'POST':
#         form = CommentForm(data=request.POST)
#         if form.is_valid():
#             comment_instance = form.save(commit=False)
#             comment_instance.post = post
#             comment_instance.user = request.user
#             comment_instance.save()
#             # messages.success(request, 'Thank you for commenting, Your comment is pending admin approval.')
#             return HttpResponse(
#                 status=204,
#                 headers= {
#                     'HX-Trigger': json.dumps({
#                         "postListChanged": None,
#                         "showMessage": f"Thank you for commenting, Your comment is pending admin approval."
#                     })
#                 }
#             )
#     else:
#         form = CommentForm()

#     context = {
#         'form': form,
#         'post': post
#     }

#     return render(request, 'htmx/comments/comment_form.html', context)
