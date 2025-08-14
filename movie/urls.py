from django.urls import path
from .views import movie_detail, movie_list, increase_view_count, admin_create_movie, admin_edit_movie, admin_delete_movie, movie_quality

urlpatterns = [
    path('list/', movie_list, name='movie-list'),
    path('<int:pk>/', movie_detail, name='movie-detail'),
    path('<int:pk>/increase-views/', increase_view_count, name='increase-view-count'),
    path('<int:pk>/quality/', movie_quality, name='movie_quality'),
    path('admin/create/', admin_create_movie, name='admin-create-movie'),
    path('admin/<int:pk>/edit/', admin_edit_movie, name='admin-edit-movie'),
    path('admin/<int:pk>/delete/', admin_delete_movie, name='admin-delete-movie'),
]
