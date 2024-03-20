from django.urls import path
from django_blog_backend.htmx_crud import views


app_name = 'htmx_crud'

urlpatterns = [
    path('', views.index, name='index'),
    path('htmx/delete-post/<int:pk>/', views.DeletePost.as_view(), name='htmx-delete-post'),
    path('htmx/post-detail/<int:pk>/', views.post_detail, name='htmx-post-detail'),
]
