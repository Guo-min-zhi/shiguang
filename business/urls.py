#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from django.conf.urls import url
from . import views

urlpatterns = [
	
	# Get all shiguang 
	# ex: /business/shiguang/all
	#url(r'^shiguang/all/(?P<uid>[0-9]+)/(?P<page>[0-9]+)/$', views.all, name='all'),
	url(r'^shiguang/all/$', views.all, name='all'),

	# Create a shiguang.
	# ex: /business/shiguang/add
	url(r'^shiguang/add/$', views.add, name='add'),

	# add a record.
	# ex: /business/shiguang/record/add/
	url(r'^shiguang/record/add/$', views.addRecord, name='addRecord'),

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
	# ex: /business/shiguang/get/month/records/
	url(r'^shiguang/get/month/records/$', views.getRecordsOfMonth, name='getRecordsOfMonth'),

	# Get record info
	# ex: /business/shiguang/get/record/info/
	url(r'^shiguang/get/record/info/$', views.getRecordInfo, name='getRecordInfo'),

	# Get all records according to shiguang id
	# ex: /business/shiguang/get/record/all/
	url(r'^shiguang/get/record/all/$', views.getAllRecordsOfShiguang, name='getAllRecordsOfShiguang'),

	# Delete one record according to record id
	# ex: /business/shiguang/record/delete/
	url(r'^shiguang/record/delete/$', views.deleteOneRecord, name='deleteOneRecord'),

	# Delete one shiguang according to shiguang id
	# ex: /business/shiguang/delete/
	url(r'^shiguang/delete/$', views.deleteOneShiguang, name='deleteOneShiguang'),

	# Complete one shiguang according to shiguang id
	# ex: /business/shiguang/complete/
	url(r'^shiguang/complete/$', views.shiguangComplete, name='shiguangComplete'),

	# Get unfinished shiguang according to user id and page.
	# ex: /business/shiguang/undone/
	url(r'^shiguang/undone/$', views.getUndoneShiguang, name='getUndoneShiguang'),

	# Root to the index page.
	# ex: /business?uid=1
	url(r'^$', views.index, name='index'),

	# Root to the shiguang index page.
	# ex: /business/shiguang?sid=1
	url(r'^shiguang/$', views.shiguangIndex, name='shiguangIndex'),

	# Root to one day page.
	# ex: /business/shiguang/record?rid=1
	url(r'^shiguang/record/$', views.recordSharePage, name='recordSharePage')
]