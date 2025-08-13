from django.urls import path
from .views import get_me, signup, login_view, update_me, admin_list_users

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', login_view, name='login'),
	path('me/', get_me, name='get_me'),
	path('me/update/', update_me, name='update_me'),
	path('admin/users/', admin_list_users, name='admin-list-users'),
]
