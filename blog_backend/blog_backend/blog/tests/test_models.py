import pytest
from django.test import TestCase

#from django.contrib.auth.models import User
from blog_backend.users.models import User
from blog_backend.blog.models import Tag, Comment, Post


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user('test', 'test@test.com', 'test')
    count = User.objects.all().count()
    print(count)
    assert User.objects.count() == 1

@pytest.mark.django_db
def test_create_taga():
    Tag.objects.create(name="Python")
    assert Tag.objects.count() == 1



class CreatePostTests(TestCase):
    def test_create_post(self):
        user = User.objects.create_user("test", "test@test.io", "test")
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )
        python_tag = Tag.objects.create(name="Python")
        django_tag = Tag.objects.create(name="Django")
        post.tag.set([python_tag.pk, django_tag.pk])
        print("The number of tags this note has is " + str(post.tag.count()))
        self.assertEqual(post.tag.count(), 2)