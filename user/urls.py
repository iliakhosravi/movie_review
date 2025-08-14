from django.urls import path
from .views import admin_delete_user, check_name_exists, get_me, signup, login_view, update_me, admin_list_users

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', login_view, name='login'),
	path('me/', get_me, name='get_me'),
    path('check-name/', check_name_exists, name='check-name-exists'),
	path('me/update/', update_me, name='update_me'),
	path('admin/users/', admin_list_users, name='admin-list-users'),
    path('admin/users/<int:pk>/delete/', admin_delete_user, name='admin-delete-user'),

]
