from django.conf.urls import url
from . import views

urlpatterns = [
	
	# Get all shiguang 
	# ex: /business/shiguang/all
	url(r'^shiguang/all/$', views.all, name='all'),
]