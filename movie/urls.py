from django.urls import path
from .views import movie_list, admin_create_movie, admin_edit_movie, admin_delete_movie

urlpatterns = [
    path('list/', movie_list, name='movie-list'),
    path('admin/create/', admin_create_movie, name='admin-create-movie'),
    path('admin/<int:pk>/edit/', admin_edit_movie, name='admin-edit-movie'),
    path('admin/<int:pk>/delete/', admin_delete_movie, name='admin-delete-movie'),
]
