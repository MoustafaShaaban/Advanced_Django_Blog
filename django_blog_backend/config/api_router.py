from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from django_blog_backend.users.api.views import UserViewSet
from django_blog_backend.api import views

router = DefaultRouter() if settings.DEBUG else SimpleRouter()

router.register("users", UserViewSet)
router.register("posts", views.PostViewSet, basename="posts")
router.register("user_posts", views.UserPostViewSet, basename="user_posts")
router.register("comments", views.CommentViewSet, basename="comments")
router.register("tags", views.TagViewSet, basename="tags")

app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("search/", views.SearchForPosts.as_view(), name="search"),
    path("favorite-post/", views.favorite_post, name="favorite-post"),
    path("like-post/", views.like_post, name="like-post"),
    # path("favorite-post/", views.AddPostToUserFavorites.as_view(), name="favorite-post"),
    path("favorite-posts/", views.UserFavoritePostListView.as_view(), name="favorite-posts-list"),
    path("user-posts/", views.UserPostsListView.as_view(), name="user-posts-list"),
    path("username/", views.username_view, name="username"),
    path('csrf/', views.get_csrf, name='csrf'),
    path('login/', views.login_view, name='login'),
]
