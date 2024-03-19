from django.urls import path
from django_blog_backend.htmx_crud import views


app_name = 'htmx_crud'

urlpatterns = [
    path('', views.index, name='index'),
    path('htmx/delete-post/<int:pk>/', views.delete_post, name='htmx-delete-post'),
]
