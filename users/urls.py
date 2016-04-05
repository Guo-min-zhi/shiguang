#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [

	#------------------- for mobile ----------------------
	# Get the phone number, and send the auth code.
	# ex: /users/auth
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

	# Modify nickname
	# ex: /users/change/nickname
	url(r'^change/nickname/$', views.changeNickname, name='changeNickname'),

	# Modify sex
	# ex: /users/change/sex
	url(r'^change/sex/$', views.changeSex, name='changeSex'),

	# Modify birthday
	# ex: /users/change/birthday
	url(r'^change/birthday/$', views.changeBirthday, name='changeBirthday'),

	# Modify password
	# ex: /users/change/password
	url(r'^change/password/$', views.changePassword, name='changePassword'),

	# Modify telephone
	# ex: /users/change/telephone
	url(r'^change/telephone/$', views.changeTelephone, name='changeTelephone'),

	# Modify telephone
	# ex: /users/change/avatar
	url(r'^change/avatar/$', views.changeAvatar, name='changeAvatar'),

	# Send authcode before find password 
	# ex: /users/find/password/before/
	url(r'^find/password/before/$', views.findPasswordBefore, name='findPasswordBefore'),

	# Verify auth code 
	# ex: /users/authcode/verify
	url(r'^authcode/verify/$', views.authcodeVerify, name='authcodeVerify'),

	# Find back password 
	# ex: /users/find/password
	url(r'^find/password/$', views.findPassword, name='findPassword'),

	# Add feedback 
	# ex: /users/add/feedback/
	url(r'^add/feedback/$', views.addFeedback, name='addFeedback'),




	#===========
	# Get all users, for test
	# ex: /users/all
	url(r'^all/$', views.all, name='all'),

	#------------------- for web page ----------------------

	url(r'^page/login/$', views.loginPage, name='loginPage'),

	url(r'^page/register/$', views.registerPage, name='registerPage'),

	url(r'^page/home/$', views.homePage, name='homePage'),

	url(r'^info/$', views.setUserInfo, name="setUserInfo")
]