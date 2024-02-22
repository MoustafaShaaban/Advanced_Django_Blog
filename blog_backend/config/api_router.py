from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter
from blog_backend.api import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("users", UserViewSet, basename="snippet")
router.register("posts", views.PostViewSet, basename="posts")
router.register("user_posts", views.UserPostViewSet, basename="user_posts")
router.register("comments", views.CommentViewSet, basename="comments")
router.register("tags", views.TagViewSet, basename="tags")


app_name = "api"

urlpatterns = router.urls

urlpatterns += [
    path("search/", views.SearchForPosts.as_view(), name="search"),
    path("favorite-post/", views.favorite_post, name="favorite-post"),
    # path("favorite-post/", views.AddPostToUserFavorites.as_view(), name="favorite-post"),
    path("favorite-posts/", views.UserFavoritePostListView.as_view(), name="favorite-posts-list"),
    path("user-posts/", views.UserPostsListView.as_view(), name="user-posts-list"),
    path("username/", views.username_view, name="username"),
]
