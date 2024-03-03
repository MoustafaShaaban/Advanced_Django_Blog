from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.conf import settings


class Tag(models.Model):
    """Model definition for Tag."""

    # TODO: Define fields here
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True)

    class Meta:
        """Meta definition for Tag."""

        verbose_name = 'tag'
        verbose_name_plural = 'tags'

    def __str__(self):
        """Unicode's representation of Tag."""
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class Post(models.Model):
    """Model definition for Post."""
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text='Post author',
        null=True,
    )
    title = models.CharField(
        max_length=250,
        unique=True,
        help_text='Post title'
    )
    slug = models.SlugField(
        max_length=250,
        unique=True,
        help_text='Post slug used in the urls instead of ids',
        null=True
    )
    content = models.TextField(help_text='Post content')
    published_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    tag = models.ManyToManyField(
        Tag,
        related_name='posts'
    )

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='favorite_posts'
    )

    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='post_likes'
    )


    class Meta:
        """Meta definition for Post."""

        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-published_at', 'author', 'updated_at'])
        ]
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        """Unicode representation of Post."""
        return f'Author: {self.author}, Post Title: {self.title}'

    def get_absolute_url(self):
        """ A method to tell Django how to calculate the canonical URL (official url of a page) for an object """
        return reverse('blog:post-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class Comment(models.Model):
    """Model definition for Comment."""

    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    comment = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(
        default=False,
        help_text='Is the comment approved by admin?'
    )

    class Meta:
        """Meta definition for Comment."""

        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['-published_at'])
        ]
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        """Unicode's representation of Comment."""
        return f'Comment by: ({self.user}) on ({self.post.title})'
