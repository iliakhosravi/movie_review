from django.urls import path
from .views import list_my_favorites

urlpatterns = [
    path('me/', list_my_favorites, name='list_my_favorites'),
]