from django.urls import path
from blog_backend.blog import views
from blog_backend.graphql_app.schema import schema

from blog_backend.graphql_app.views import PrivateGraphQLView


app_name = 'blog'

urlpatterns = [
    # URLs for Blog posts CRUD operations:
    path('', views.HomePage.as_view(), name='homepage'),
    path('create-post/', views.CreatePost.as_view(), name='create-post'),
    path('update/post/<slug:slug>/', views.UpdatePost.as_view(), name='update-post'),
    path('delete/post/<slug:slug>/', views.DeletePost.as_view(), name='delete-post'),

    # URLs for post details and user posts and favorite posts:
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('favorite-post/<slug:slug>/', views.favorite_post, name='favorite_post'),

    path('user-post-list/', views.UserPostView.as_view(), name='user-post-list'),
    path('profile/favorites/', views.UserfavoritePostListView.as_view(), name='favorite-post-list'),

    # URL for adding comments to blog posts:
    path('<slug:slug>/create-comment/', views.create_comment, name='create-comment'),

    # URL for listing all tags:
    path('tags/', views.tag_list, name='tag-list'),

    # URL for Listing Blog posts by tag
    path('tag/<slug:slug>/',views.tag_post_list, name='tag-post-list'),

    # URL for GraphQL endpoint:
    path("graphql/", PrivateGraphQLView.as_view(graphiql=True, schema=schema), name="graphql"),

    # URL for searching the Blog:
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
]
