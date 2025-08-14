from django.urls import path
from .views import create_comment, delete_my_comment, edit_my_comment, get_comment_by_id, list_comments_by_movie, admin_delete_comment, list_my_comments

urlpatterns = [
    path('create/', create_comment, name='create-comment'),
    path('me/', list_my_comments, name='list-my-comments'),
    path('movie/<int:movie_id>/', list_comments_by_movie, name='list-comments-by-movie'),
    path('admin/<int:pk>/delete/', admin_delete_comment, name='admin-delete-comment'),
    path('me/<int:pk>/delete/', delete_my_comment, name='delete-my-comment'),
    path('<int:pk>/', get_comment_by_id, name='get-comment-by-id'),
    path('me/<int:pk>/edit/', edit_my_comment, name='edit-my-comment'),
]
