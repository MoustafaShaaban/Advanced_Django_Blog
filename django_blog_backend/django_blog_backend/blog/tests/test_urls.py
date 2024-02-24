import uuid
import pytest

from django.test import TestCase
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django_blog_backend.users.models import User
from django_blog_backend.blog.models import Tag, Comment, Post


def createUser():
    return User.objects.create_user("test", "test@test.com", "test")

class HomepageTests(TestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("blog:homepage"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("blog:homepage"))
        self.assertTemplateUsed(response, "blog/index.html")


class CreatePostTests(TestCase):

    def test_url_exists_at_correct_location(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:create-post"))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:create-post"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:create-post"))
        self.assertTemplateUsed(response, "blog/posts/create_post.html")


class UpdatePostTests(TestCase):

    def test_url_exists_at_correct_location(self):
        user = createUser()
        self.client.force_login(user=user)
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )

        response = self.client.get(reverse("blog:update-post", kwargs={'slug':post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        user = createUser()
        self.client.force_login(user=user)
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )
        python_tag = Tag.objects.create(name="Python")
        django_tag = Tag.objects.create(name="Django")
        post.tag.set([python_tag.pk, django_tag.pk])
        response = self.client.get(reverse("blog:update-post", kwargs={'slug':post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        user = createUser()
        self.client.force_login(user=user)
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )
        python_tag = Tag.objects.create(name="Python")
        django_tag = Tag.objects.create(name="Django")
        post.tag.set([python_tag.pk, django_tag.pk])
        response = self.client.get(reverse("blog:update-post", kwargs={'slug':post.slug}))
        self.assertTemplateUsed(response, "blog/posts/update_post.html")



class DeletePostTests(TestCase):

    def test_url_exists_at_correct_location(self):
        user = createUser()
        self.client.force_login(user=user)
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )
        python_tag = Tag.objects.create(name="Python")
        django_tag = Tag.objects.create(name="Django")
        post.tag.set([python_tag.pk, django_tag.pk])
        response = self.client.get(reverse("blog:delete-post", kwargs={'slug':post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        user = createUser()
        self.client.force_login(user=user)
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )
        python_tag = Tag.objects.create(name="Python")
        django_tag = Tag.objects.create(name="Django")
        post.tag.set([python_tag.pk, django_tag.pk])
        response = self.client.get(reverse("blog:delete-post", kwargs={'slug':post.slug}))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        user = createUser()
        self.client.force_login(user=user)
        post = Post.objects.create(
            title="Post 1",
            content="Post 1 content",
            author=user,
        )
        python_tag = Tag.objects.create(name="Python")
        django_tag = Tag.objects.create(name="Django")
        post.tag.set([python_tag.pk, django_tag.pk])
        response = self.client.get(reverse("blog:delete-post", kwargs={'slug':post.slug}))
        self.assertTemplateUsed(response, "blog/posts/delete_post.html")


class UserPostListTests(TestCase):

    def test_url_exists_at_correct_location(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:user-post-list"))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:user-post-list"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:user-post-list"))
        self.assertTemplateUsed(response, "blog/posts/user_post_list.html")


class UserFavoritePostListTests(TestCase):

    def test_url_exists_at_correct_location(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:favorite-post-list"))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:favorite-post-list"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:favorite-post-list"))
        self.assertTemplateUsed(response, "blog/posts/user_favorite_post_list.html")


class TagtListTests(TestCase):

    def test_url_exists_at_correct_location(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:tag-list"))
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:tag-list"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        user = createUser()
        self.client.force_login(user=user)
        response = self.client.get(reverse("blog:tag-list"))
        self.assertTemplateUsed(response, "blog/tags.html")



# @pytest.mark.django_db
# def test_create_blog_post_view(admin_client):
#     url = reverse_lazy('blog:create-post')
#     response = admin_client.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_user_post_list_view(admin_client):
#     url = reverse_lazy('blog:user-post-list')
#     response = admin_client.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_user_favorite_post_list_view(admin_client):
#     url = reverse_lazy('blog:favorite-post-list')
#     response = admin_client.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_tags_list_view(admin_client):
#     url = reverse_lazy('blog:tag-list')
#     response = admin_client.get(url)
#     assert response.status_code == 200


# class TestAuthPage(TestCase):
#     def test_tags_page(self):
#         user = User.objects.create_user("Juliana," "juliana@dev.com", "some_pass")
#         self.client.force_login(user=user)
#         response = self.client.get(reverse('blog:homepage'))
#         self.assertEqual(response.status_code, 200)
