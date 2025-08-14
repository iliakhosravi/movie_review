from django.urls import path
from .views import delete_favorite, list_my_favorites, create_favorite

urlpatterns = [
    path('me/', list_my_favorites, name='list_my_favorites'),
    path('<int:pk>/delete/', delete_favorite, name='delete-favorite'),
    path('create/', create_favorite, name='create-favorite'),


]