from django.urls import path
from .views import create_comment, list_comments_by_movie, admin_delete_comment

urlpatterns = [
    path('create/', create_comment, name='create-comment'),
    path('movie/<int:movie_id>/', list_comments_by_movie, name='list-comments-by-movie'),
    path('admin/<int:pk>/delete/', admin_delete_comment, name='admin-delete-comment'),
]
