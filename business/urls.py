from django.conf.urls import url
from . import views

urlpatterns = [
	
	# Get all shiguang 
	# ex: /business/shiguang/all
	url(r'^shiguang/all/(?P<uid>[0-9]+)/$', views.all, name='all'),

	# Create a shiguang.
	# ex: /business/shiguang/add
	url(r'^shiguang/add/$', views.add, name='add'),

	# Get old shiguang has 5 size limit
	# ex: /business/shiguang/get/old
	url(r'^shiguang/get/old/$', views.getLineOldPage, name='getLineOldPage'),

	# Get new shiguang 
	# ex: /business/shiguang/get/new
	url(r'^shiguang/get/new/$', views.getLineNew, name='getLineNew'),

	# Get old unfinished shiguang 
	# ex: /business/shiguang/get/undone/old
	url(r'^shiguang/get/undone/old/$', views.getUndoneOldPage, name='getUndoneOldPage'),

	# Get new unfinished shiguang 
	# ex: /business/shiguang/get/undone/new
	url(r'^shiguang/get/undone/new/$', views.getUndoneNew, name='getUndoneNew'),

	# Get records of one month of shiguang
	# ex:
	url(r'^shiguang/get/month/records/$', views.getRecordsOfMonth, name='getRecordsOfMonth'),

	# Get record info
	# ex:
	url(r'^shiguang/get/record/info/$', views.getRecordInfo, name='getRecordInfo'),
]