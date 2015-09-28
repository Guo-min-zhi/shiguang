from django.db import models
from users.models import User

# Create your models here.

class Shiguang(models.Model):
	"""docstring for Shiguang"""
	# name
	theme = models.CharField(max_length=100)
	# description
	description = models.CharField(max_length=2000)
	# create time
	create_time = models.DateTimeField(auto_now_add=True)

	#start time
	start_time = models.DateTimeField(null=True, blank=True)
	# end time
	end_time = models.DateTimeField(null=True, blank=True)
	# tag one
	# LIFE = 'LIFE'
	# WORK = 'WORK'
	# FIRST_LEVEL_TAG = (
	# 	(LIFE, 'life'),
	# 	(WORK, 'work'),
	# )
	# first_level_tag = models.CharField(max_length=100,choices=FIRST_LEVEL_TAG)
	# tag two
	tags = models.CharField(max_length=200, null=True, blank=True)
	# tag three

	# cover
	cover = models.CharField(max_length=100, null=True, blank=True)
	# user, foreign key
	user = models.ForeignKey(User)

class Record(models.Model):
	"""docstring for record"""
	content = models.CharField(max_length=1000)
	create_time = models.DateTimeField(auto_now_add=True)
	shiguang = models.ForeignKey(Shiguang)

class RecordPicture(models.Model):
	"""docstring for record picture"""
	upload_time = models.DateTimeField(auto_now_add=True)
	picture = models.CharField(max_length=100, null=True, blank=True)
	record = models.ForeignKey(Record)













