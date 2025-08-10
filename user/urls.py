from django.urls import path
from .views import signup, login_view, update_me

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', login_view, name='login'),
	path('me/', update_me, name='update_me'),
]
