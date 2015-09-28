from django.conf.urls import url
from . import views


urlpatterns = [

	# Get the phone number, and send the auth code.
	# ex: /users/code
	url(r'^auth/$', views.auth, name='authCode'),
	# User Register
	# ex: /users/register
	url(r'^register/$', views.register, name='register'),

	# User Login
	# ex: /users/login
	url(r'^login/$', views.login, name='login'),

	# Get user infomation
	# ex: /users/info/{userid}
	url(r'^userInfo/$', views.userInfo, name='userInfo'),

	#===========
	# Get all users, for test
	# ex: /users/all
	url(r'all/$', views.all, name='all'),
]