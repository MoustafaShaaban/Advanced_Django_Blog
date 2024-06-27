from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin


from .models import Post, Tag, Comment
from .forms import CommentForm


class HomePage(generic.ListView):
    """Home page that shows all posts with maximum 5 posts per page."""
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 5


class SearchResultsView(generic.ListView):
    """ A view to show user's search results """
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get("q")
        search_results = Post.objects.filter(
            Q(title__icontains=query)
        )
        return search_results


class UserPostView(LoginRequiredMixin, generic.ListView):
    """ A view to show a list of the user's posts """
    model = Post
    template_name = 'blog/posts/user_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-published_at')


class UserFavoritePostListView(LoginRequiredMixin, generic.ListView):
    """ A view to show a list of the user's favorite posts """
    model = Post
    template_name = 'blog/posts/user_favorite_post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(favorites=self.request.user).order_by('-published_at')


class CreatePost(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    """ A view to add a new post. """
    model = Post
    fields = ['title', 'content', 'tag']
    template_name = 'blog/posts/create_post.html'
    success_url = reverse_lazy('blog:homepage')
    success_message = "Post Added Successfully"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """ A view to update a specific post. """
    model = Post
    fields = ['title', 'content', 'tag']
    template_name = 'blog/posts/update_post.html'
    # success_url = reverse_lazy('blog:homepage')
    success_message = "Post Updated Successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.object.slug})


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """ A view to delete a specific post. """
    model = Post
    template_name = 'blog/posts/delete_post.html'
    success_url = reverse_lazy('blog:homepage')
    success_message = "Post Deleted Successfully"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def post_detail(request, slug):
    """Show a single post with all its tags and comments."""
    post = get_object_or_404(Post, slug=slug)
    tags = post.tag.all()
    comments = post.comments.filter(approved=True).order_by('-published_at')
    form = CommentForm()

    context = {
        'post': post,
        'tags': tags,
        'comments': comments,
        'form': form,
    }

    return render(request, 'blog/posts/post_detail.html', context)


@login_required
def create_comment(request, slug):
    """Add a comment."""
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment_instance = form.save(commit=False)
            comment_instance.post = post
            comment_instance.user = request.user
            comment_instance.save()
            messages.success(request, 'Thank you for commenting, Your comment is pending admin approval.')
            return redirect('blog:post-detail', post.slug)
    else:
        form = CommentForm()

    context = {
        'form': form,
        'post': post,
    }
    return render(request, 'blog/comments/create_comment.html', context)


class UpdateComment(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.UpdateView):
    """ A view to update a specific post. """
    model = Comment
    fields = ['comment']
    template_name = 'blog/comments/update_comment.html'
    # success_url = reverse_lazy('blog:homepage')
    success_message = "Comment Updated Successfully"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.object.post.slug})


class DeleteComment(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, generic.DeleteView):
    """ A view to delete a specific post. """
    model = Comment
    template_name = 'blog/comments/delete_comment.html'
    # success_url = reverse_lazy('blog:homepage')
    success_message = "Comment Deleted Successfully"

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'slug': self.object.post.slug})


@login_required
def favorite_post(request, slug):
    """ A view to add a post to the user's favorites """
    if request.method == 'POST':
        post = Post.objects.get(slug=slug)
        if not post.favorites.filter(id=request.user.id).exists():
            post.favorites.add(request.user)
            post.save()
            messages.success(request, 'Added post to your favorites.')

            context = {'post': post}
            return render(
                request,
                'blog/posts/partials/favorite_post.html',
                context
            )
        else:
            post.favorites.remove(request.user)
            post.save()
            messages.success(request, 'Removed post from your favorites.')

            context = {'post': post}
            return render(
                request,
                'blog/posts/partials/favorite_post.html',
                context
            )


@login_required
def like_post(request, slug):
    """ A view to add a post to the user's favorites """
    if request.method == 'POST':
        post = Post.objects.get(slug=slug)
        if not post.likes.filter(id=request.user.id).exists():
            post.likes.add(request.user)
            post.save()
            messages.success(request, 'Liked post.')

            context = {'post': post}
            return render(
                request,
                'blog/posts/partials/like_post.html',
                context
            )
        else:
            post.likes.remove(request.user)
            post.save()
            messages.success(request, 'Unliked post.')

            context = {'post': post}
            return render(
                request,
                'blog/posts/partials/like_post.html',
                context
            )


@login_required
def tag_list(request):
    """ A view to show a list of the available tags in the blog. """
    tag_list = Tag.objects.all()
    context = {'tag_list': tag_list}
    return render(request, 'blog/tags.html', context)


@login_required
def tag_post_list(request, slug):
    """ A view to filter the posts by tags. """
    tags = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    posts = Post.objects.filter(tag=tags)
    context = {
        'tags': tags,
        'posts': posts,
    }

    return render(request, 'blog/posts/tags_post_list.html', context)
