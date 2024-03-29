from django.urls import path
from django_blog_backend.htmx_crud import views


app_name = 'htmx_crud'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.post_list, name='post_list'),
    path('posts/add', views.add_post, name='add_post'),
    path('posts/<int:pk>/edit', views.edit_post, name='edit_post'),
    path('htmx/delete-post/<int:pk>/', views.remove_post, name='delete-post'),
    path('htmx/update-post/<int:pk>/', views.HTMXUpdatePostView.as_view(), name='htmx-update-post'),
    path('<int:pk>/create-comment/', views.create_comment, name='create-comment'),
    #path('htmx/post-detail/<int:pk>/', views.post_detail, name='htmx-post-detail'),
]
