from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import Http404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy


from .models import Post, Comment, Tag
from .forms import CommentForm


class HomePage(generic.ListView):
	"""Home page that shows all posts with maximum 5 posts per page."""
	model = Post
	template_name = 'blog/index.html'
	context_object_name = 'posts'
	paginate_by = 5


class UserPostView(LoginRequiredMixin, generic.ListView):
	model = Post
	template_name = 'blog/posts/user_post_list.html'
	context_object_name = 'posts'
	paginate_by = 5

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user).order_by('-published_at')



def post_detail(request, slug):
	"""Show a single post with all its tags and comments."""
	post = get_object_or_404(Post, slug=slug)
	tags = post.tag.all()
	comments = post.comments.filter(approved=True).order_by('-published_at')


	context = {
		'post': post,
		'tags': tags,
		'comments': comments,
	}

	return render(request, 'blog/posts/post_detail.html', context)


def create_comment(request, slug):
	"""Add a comment."""
	post = get_object_or_404(Post, slug=slug)

	if request.method != 'POST':
		form = CommentForm()
	else:
		form = CommentForm(data=request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.post = post
			new_comment.name = request.user
			new_comment.save()
			messages.success(request, 'Thank you for commenting, Your comment is pending admin approval.')
			return redirect('blog:post-detail', post.slug)
	
	context = {
		'form': form,
		'post': post,
	}
	return render(request, 'blog/posts/create_comment.html', context)


def tag_list(request):
	tag_list = Tag.objects.all()
	context = {'tag_list': tag_list}
	return render(request, 'blog/tags.html', context)


def tag_post_list(request, slug):
	tags = get_object_or_404(Tag, slug=slug)
	# Filter posts by tag name  
	posts = Post.objects.filter(tag=tags)
	context = {
		'tags':tags,
		'posts':posts,
	}

	return render(request, 'blog/posts/tags_post_list.html', context)


class CreatePost(LoginRequiredMixin, generic.CreateView):
	model = Post
	fields = ['title', 'content', 'tag']
	template_name = 'blog/posts/create_post.html'
	success_url = reverse_lazy('blog:homepage')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
	model = Post
	fields = ['title', 'content', 'tag']
	template_name = 'blog/posts/update_post.html'
	success_url = reverse_lazy('blog:homepage')

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
	model = Post
	template_name = 'blog/posts/delete_post.html'
	success_url = reverse_lazy('blog:homepage')

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False