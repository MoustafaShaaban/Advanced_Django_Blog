from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


class Tag(models.Model):
    """Model definition for Tag."""

    # TODO: Define fields here
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        """Unicode representation of Tag."""
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Post(models.Model):
    """Model definition for Post."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Post author'
    )
    title = models.CharField(
        max_length=250, 
        unique=True, 
        help_text='Post title'
    )
    slug = models.SlugField(
        max_length=250, 
        unique=True, 
        help_text='Post slug used in the urls instead of ids'
    )
    content = models.TextField(help_text='Post content')
    published_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    tag = models.ManyToManyField(
        Tag,
        related_name='tags'
    )


    class Meta:
        """Meta definition for Post."""

        ordering = ['-updated_at']
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        """Unicode representation of Post."""
        return f'Author: {self.author}, Post: {self.title}'

    def get_absolute_url(self):
        """ A method to tell Django how to calculate the canonical URL (official url of a page) for an object """
        return reverse('post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    """Model definition for Comment."""

    # TODO: Define fields here
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(
        default=False, 
        help_text='Is the comment approved by admin?'
    )



    class Meta:
        """Meta definition for Comment."""

        ordering = ['-published_at']
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        """Unicode representation of Comment."""
        return f'Comment by: {self.name} on {self.post}'
