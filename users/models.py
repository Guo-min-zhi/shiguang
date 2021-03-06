#!/usr/local/bin/python
#-*- coding:utf-8 -*-
from django.db import models

# Create your models here.

class User(models.Model):
	""" The user of our system """
	# phone country code
	phone_country_code = models.CharField(max_length=20, default='86')
	# phone number
	phone_number = models.CharField(max_length=100, unique=True)
	# nick name
	nick_name = models.CharField(max_length=100, blank=True)
	# real name
	real_name = models.CharField(max_length=100, blank=True)
	# sex, 1 for male, 0 for female.
	sex = models.IntegerField(default=0, blank=True)
	# birthday
	birthday = models.DateField(blank=True, null=True)
	# email
	email = models.EmailField(blank=True)
	# avatar path
	avatar_path = models.CharField(max_length=200, blank=True)
	#avatar_path = models.ImageField(upload_to='avatar', blank=True)
	# register date
	register_date = models.DateTimeField(auto_now_add=True)
	# password
	password = models.CharField(max_length=100,blank=True)

	def __str__(self):
		return self.nick_name

class Authcode(models.Model):
	""" Auth code temp entity """
	# phone country code
	phone_country_code = models.CharField(max_length=20, default='86')
	# phone number
	phone_number = models.CharField(max_length=100)
	# auth code
	code = models.IntegerField()
	# send time
	send_time = models.DateTimeField(auto_now_add=True)

class AuthcodeHistory(models.Model):
	""" Auth code history entity """
	# phone number
	phone_number = models.CharField(max_length=100)
	# auth code
	auth_code = models.IntegerField()
	# send time
	send_time = models.DateTimeField()

class FeedBack(models.Model):
	"""docstring for FeedBack"""
	create_time = models.DateTimeField(auto_now_add=True)
	feedback = models.CharField(max_length=200, null=True, blank=True)
	contact = models.CharField(max_length=50, null=True, blank=True)
	user = models.ForeignKey(User)







