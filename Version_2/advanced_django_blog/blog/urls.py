from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path("search/", views.SearchResultsView.as_view(), name="search_results"),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('favorite-post/<slug:slug>/', views.favorite_post, name='favorite-post'),
    path('tags/', views.tag_list, name='tag-list'),
    path('profile/', views.UserPostView.as_view(), name='profile'),
    path('profile/favorites/', views.UserfavoritePostListView.as_view(), name='favorite-post-list'),
    path('create-post/', views.CreatePost.as_view(), name='create-post'),
    path('<slug:slug>/create-comment/', views.post_detail, name='create-comment'),
    path('update/post/<slug:slug>/', views.UpdatePost.as_view(), name='update-post'),
    path('delete/post/<slug:slug>/', views.DeletePost.as_view(), name='delete-post'),
    path('tag/<slug:slug>/',views.tag_post_list, name='tag-post-list'),
]