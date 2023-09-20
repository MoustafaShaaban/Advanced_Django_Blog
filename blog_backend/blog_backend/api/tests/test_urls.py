import pytest

from django.urls import reverse

from blog_backend.users.models import User


@pytest.mark.django_db
def test_posts_api_endpoint(client):
    user = User.objects.create_user(username="test", email="test@test.com", password="test")
    url = reverse('api:posts-list')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_comments_api_endpoint(client):
    user = User.objects.create_user(username="test", email="test@test.com", password="test")
    url = reverse('api:comments-list')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_tags_api_endpoint(client):
    user = User.objects.create_user(username="test", email="test@test.com", password="test")
    url = reverse('api:tags-list')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_posts_api_endpoint(client):
    user = User.objects.create_user(username="test", email="test@test.com", password="test")
    url = reverse('api:user_posts-list')
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200