from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from blog_backend.users.api.views import UserViewSet
from blog_backend.api.views import PostViewSet, UserPostViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

#router.register("users", UserViewSet, basename="snippet")
router.register("posts", PostViewSet, basename="posts")
router.register("user_posts", UserPostViewSet, basename="user_posts")


app_name = "api"
urlpatterns = router.urls
