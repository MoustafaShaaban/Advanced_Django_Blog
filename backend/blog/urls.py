from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.HomePage.as_view(), name='homepage'),
    path('post/<slug:slug>/', views.post_detail, name='post-detail'),
    path('tags/', views.tag_list, name='tag-list'),
    path('profile/', views.UserPostView.as_view(), name='profile'),
    path('create-post/', views.CreatePost.as_view(), name='create-post'),
    path('<slug:slug>/create-comment/', views.create_comment, name='create-comment'),
    path('update/post/<slug:slug>/', views.UpdatePost.as_view(), name='update-post'),
    path('delete/post/<slug:slug>/', views.DeletePost.as_view(), name='delete-post'),
    path('tag/<slug:slug>/',views.tag_post_list, name='tag-post-list'),
]